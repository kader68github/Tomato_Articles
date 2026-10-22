#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
animate_calligraphy.py — Animation des ornements (oiseaux & fleurs) d'affiches
de calligraphie arabe, SANS JAMAIS modifier le texte.

Principe « sanctuaire de texte » (garantie centrale du script)
--------------------------------------------------------------
1. Chaque ligne de calligraphie est déclarée dans un fichier de configuration
   JSON sous forme de rectangle normalisé (coordonnées 0..1).
2. Ces rectangles forment un masque de protection dont le CŒUR vaut
   exactement 1.0 : à chaque image générée, la dernière opération du pipeline
   réinjecte les pixels ORIGINAUX dans ce cœur. Le texte rendu est donc
   bit-à-bit identique à l'image source (vérifiable avec ``--verify``).
3. Tous les effets (déformation des fleurs, sprites d'oiseaux, pétales,
   scintillement des dorures) sont en outre atténués à zéro dans une zone
   tampon autour du texte : aucun effet ne « fuit » sur les lettres, les
   oiseaux passent visuellement DERRIÈRE le plan du texte.

Effets d'animation (uniquement sur les ornements)
--------------------------------------------------
- Fleurs    : balancement au vent + « respiration » (pulsation radiale douce)
              par champ de déplacement sinusoïdal (cv2.remap), pondéré par des
              gaussiennes centrées sur chaque fleur déclarée.
- Végétation: brise globale très légère, pondérée par la saturation et la
              proximité des bordures (là où vivent les ornements).
- Oiseaux   : deux moteurs au choix (``bird_engine``).
              * ``warp`` (défaut, recommandé pour ces illustrations) : l'oiseau
                et son voisinage immédiat sont déplacés par le même champ de
                déformation que les fleurs (gaussienne elliptique) — dérive en
                lissajous, bobbing, rotation légère et « battement d'ailes »
                par compression anisotrope autour du corps. Aucun détourage,
                donc aucun halo ni couture.
              * ``sprite`` : détourage GrabCut + fond reconstruit par
                inpainting (Telea) + recomposition du sprite transformé.
                Permet des amplitudes plus grandes, au prix d'un léger halo
                possible sur fonds unis (colombe blanche sur crème…).
              Mode « perched » (posé) : micro-respiration seulement.
              Mode « butterfly » : les ailes se referment vers le corps.
- Dorures   : vague de lumière diagonale qui fait scintiller les pixels dorés
              (détection HSV), hors zone de texte.
- Pétales   : particules de pétales dérivant dans les bordures uniquement,
              elles s'estompent à l'approche du texte.

Toutes les fonctions temporelles utilisent un nombre ENTIER de cycles sur la
durée totale : la vidéo boucle parfaitement (première image == image à t=1).

Exemples
--------
    # Rendre une affiche (MP4 + GIF), avec vérification d'intégrité du texte
    python animate_calligraphy.py render images/03_creme_bordeaux.jpg \\
        --config configs/03_creme_bordeaux.json --verify

    # Contrôler visuellement les zones (texte / oiseaux / fleurs)
    python animate_calligraphy.py preview images/03_creme_bordeaux.jpg \\
        --config configs/03_creme_bordeaux.json

    # Rendre les 4 affiches d'un coup
    python animate_calligraphy.py batch --configs configs --output-dir output

    # Créer un modèle de configuration pour une nouvelle image
    python animate_calligraphy.py init-config ma_photo.jpg

Prérequis : Python >= 3.10, opencv-python-headless, numpy, Pillow,
            imageio + imageio-ffmpeg (encodage H.264 propre).

Auteur  : généré pour le projet Tomato_Articles / calligraphy_animator
Licence : MIT
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import sys
import time
from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Any, Iterable, Iterator, Sequence

import cv2
import numpy as np

__version__ = "1.0.0"
__all__ = [
    "BirdMode",
    "BirdZone",
    "CalligraphyAnimator",
    "EffectsConfig",
    "FlowerZone",
    "RenderOptions",
    "SceneConfig",
    "TextZone",
    "main",
]

LOGGER = logging.getLogger("animate_calligraphy")

TAU = 2.0 * math.pi


# ---------------------------------------------------------------------------
# Petites fonctions utilitaires
# ---------------------------------------------------------------------------
def osc(t: float | np.ndarray, cycles: int, phase: float = 0.0) -> float | np.ndarray:
    """Oscillation sinusoïdale bouclable : ``sin(2π(cycles·t + phase))``.

    ``cycles`` est un entier ⇒ ``osc(0) == osc(1)`` : la boucle est parfaite.
    Fonctionne aussi bien sur un scalaire que sur un tableau NumPy.
    """
    return np.sin(TAU * (cycles * t + phase))


def _check_unit(name: str, value: float, *, allow_zero: bool = True) -> None:
    """Valide qu'une coordonnée normalisée est bien dans [0, 1]."""
    low_ok = value >= 0.0 if allow_zero else value > 0.0
    if not (low_ok and value <= 1.0):
        raise ValueError(f"{name} = {value!r} hors de l'intervalle [0, 1]")


def hex_to_bgr(color: str) -> tuple[int, int, int]:
    """``'#e8a7bf'`` → tuple BGR OpenCV."""
    c = color.lstrip("#")
    if len(c) != 6:
        raise ValueError(f"Couleur hexadécimale invalide : {color!r}")
    r, g, b = (int(c[i : i + 2], 16) for i in (0, 2, 4))
    return b, g, r


def imread_unicode(path: Path) -> np.ndarray:
    """Lecture d'image robuste aux chemins non-ASCII (Windows inclus)."""
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Image illisible ou format non pris en charge : {path}")
    return img


def imwrite_unicode(path: Path, img: np.ndarray, quality: int = 92) -> None:
    """Écriture d'image robuste aux chemins non-ASCII."""
    suffix = path.suffix.lower() or ".jpg"
    params = [cv2.IMWRITE_JPEG_QUALITY, quality] if suffix in {".jpg", ".jpeg"} else []
    ok, buf = cv2.imencode(suffix, img, params)
    if not ok:
        raise IOError(f"Encodage impossible vers {path}")
    buf.tofile(str(path))


def even(value: int) -> int:
    """Rend une dimension paire (exigence des encodeurs H.264/yuv420p)."""
    return value if value % 2 == 0 else value - 1


# ---------------------------------------------------------------------------
# Modèle de configuration (fichiers JSON dans configs/)
# ---------------------------------------------------------------------------
class BirdMode(str, Enum):
    """Comportement d'animation d'un sujet détouré."""

    HOVER = "hover"          # en vol stationnaire (oiseaux en plein vol)
    PERCHED = "perched"      # posé sur une branche : micro-mouvements
    BUTTERFLY = "butterfly"  # papillon : compression horizontale des ailes


@dataclass(slots=True)
class NormRect:
    """Rectangle en coordonnées normalisées (x, y = coin haut-gauche)."""

    x: float
    y: float
    w: float
    h: float

    def validate(self, ctx: str) -> None:
        for name, v in (("x", self.x), ("y", self.y)):
            _check_unit(f"{ctx}.{name}", v)
        for name, v in (("w", self.w), ("h", self.h)):
            _check_unit(f"{ctx}.{name}", v, allow_zero=False)
        if self.x + self.w > 1.0001 or self.y + self.h > 1.0001:
            raise ValueError(f"{ctx} déborde de l'image : {self!r}")

    def to_pixels(self, width: int, height: int, expand_px: int = 0) -> tuple[int, int, int, int]:
        """Convertit en (x0, y0, x1, y1) pixels, éventuellement dilaté."""
        x0 = max(0, int(round(self.x * width)) - expand_px)
        y0 = max(0, int(round(self.y * height)) - expand_px)
        x1 = min(width, int(round((self.x + self.w) * width)) + expand_px)
        y1 = min(height, int(round((self.y + self.h) * height)) + expand_px)
        return x0, y0, x1, y1

    @classmethod
    def from_seq(cls, seq: Sequence[float], ctx: str) -> "NormRect":
        if len(seq) != 4:
            raise ValueError(f"{ctx} doit contenir 4 nombres [x, y, w, h], reçu : {seq!r}")
        rect = cls(*(float(v) for v in seq))
        rect.validate(ctx)
        return rect

    def to_list(self) -> list[float]:
        return [round(self.x, 4), round(self.y, 4), round(self.w, 4), round(self.h, 4)]


@dataclass(slots=True)
class TextZone:
    """Une ligne (ou un bloc) de calligraphie à protéger intégralement."""

    rect: NormRect
    label: str = "texte"

    @classmethod
    def from_dict(cls, data: dict[str, Any], idx: int) -> "TextZone":
        if "rect" in data:
            rect = NormRect.from_seq(data["rect"], f"text_zones[{idx}].rect")
        else:  # forme courte {x, y, w, h}
            rect = NormRect(float(data["x"]), float(data["y"]), float(data["w"]), float(data["h"]))
            rect.validate(f"text_zones[{idx}]")
        return cls(rect=rect, label=str(data.get("label", f"ligne {idx + 1}")))

    def to_dict(self) -> dict[str, Any]:
        return {"rect": self.rect.to_list(), "label": self.label}


@dataclass(slots=True)
class BirdZone:
    """Un oiseau (ou papillon) à détourer puis animer en sprite."""

    bbox: NormRect
    mode: BirdMode = BirdMode.HOVER
    label: str = "oiseau"
    phase: float = 0.0            # déphasage temporel 0..1 (évite la synchro robotique)
    amplitude_px: float = 8.0     # amplitude de dérive (pixels, à résolution native)
    flutter: float = 0.055        # intensité du « battement » (compression relative)
    flutter_cycles: int = 12      # battements par boucle complète
    bob_cycles: int = 2           # montées/descentes par boucle
    rotation_deg: float = 2.6     # balancement angulaire maximal

    @classmethod
    def from_dict(cls, data: dict[str, Any], idx: int) -> "BirdZone":
        bbox = NormRect.from_seq(data["bbox"], f"birds[{idx}].bbox")
        try:
            mode = BirdMode(str(data.get("mode", "hover")).lower())
        except ValueError as exc:
            raise ValueError(
                f"birds[{idx}].mode invalide : {data.get('mode')!r} "
                f"(attendu : hover | perched | butterfly)"
            ) from exc
        return cls(
            bbox=bbox,
            mode=mode,
            label=str(data.get("label", f"oiseau {idx + 1}")),
            phase=float(data.get("phase", (idx * 0.37) % 1.0)),
            amplitude_px=float(data.get("amplitude_px", 8.0)),
            flutter=float(data.get("flutter", 0.055)),
            flutter_cycles=int(data.get("flutter_cycles", 12)),
            bob_cycles=int(data.get("bob_cycles", 2)),
            rotation_deg=float(data.get("rotation_deg", 2.6)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "bbox": self.bbox.to_list(),
            "mode": self.mode.value,
            "label": self.label,
            "phase": round(self.phase, 3),
            "amplitude_px": self.amplitude_px,
            "flutter": self.flutter,
            "flutter_cycles": self.flutter_cycles,
        }


@dataclass(slots=True)
class FlowerZone:
    """Une fleur (ou un bouquet) soumise au vent : centre + rayon normalisés."""

    cx: float
    cy: float
    radius: float = 0.06          # rayon relatif à la LARGEUR de l'image
    label: str = "fleur"
    phase: float = 0.0
    sway_px: float = 5.0          # amplitude de balancement (pixels natifs)
    breathe: float = 0.018        # pulsation radiale relative (1.8 %)
    cycles: int = 2               # oscillations par boucle

    @classmethod
    def from_dict(cls, data: dict[str, Any], idx: int) -> "FlowerZone":
        if "center" in data:
            cx, cy = (float(v) for v in data["center"])
        else:
            cx, cy = float(data["cx"]), float(data["cy"])
        _check_unit(f"flowers[{idx}].cx", cx)
        _check_unit(f"flowers[{idx}].cy", cy)
        radius = float(data.get("radius", 0.06))
        if not (0.0 < radius <= 0.5):
            raise ValueError(f"flowers[{idx}].radius invalide : {radius!r}")
        return cls(
            cx=cx,
            cy=cy,
            radius=radius,
            label=str(data.get("label", f"fleur {idx + 1}")),
            phase=float(data.get("phase", (idx * 0.29) % 1.0)),
            sway_px=float(data.get("sway_px", 5.0)),
            breathe=float(data.get("breathe", 0.018)),
            cycles=int(data.get("cycles", 2)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "center": [round(self.cx, 4), round(self.cy, 4)],
            "radius": round(self.radius, 4),
            "label": self.label,
            "phase": round(self.phase, 3),
            "sway_px": self.sway_px,
            "breathe": self.breathe,
        }


@dataclass(slots=True)
class EffectsConfig:
    """Réglages globaux des effets (surchargeables en ligne de commande)."""

    flowers: bool = True
    birds: bool = True
    bird_engine: str = "warp"                     # "warp" (sans halo) ou "sprite" (GrabCut)
    shimmer: bool = True                          # scintillement des dorures
    petals: bool = True                           # pétales dérivants (bordures)
    wind_px: float = 2.2                          # brise globale sur la végétation
    petal_count: int = 14
    petal_colors: tuple[str, ...] = ("#e8a7bf", "#d97b9c", "#f2c9d4", "#c95d7f", "#f6e3ec")
    protect_margin_px: int = 8                    # dilatation de sécurité autour du texte
    protect_feather_px: int = 16                  # fondu du masque, À L'EXTÉRIEUR du cœur
    seed: int = 42

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> "EffectsConfig":
        if not data:
            return cls()
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        kwargs: dict[str, Any] = {}
        for key, value in data.items():
            if key.startswith("_") or key not in known:
                continue
            kwargs[key] = tuple(value) if key == "petal_colors" else value
        return cls(**kwargs)

    def to_dict(self) -> dict[str, Any]:
        data = {k: getattr(self, k) for k in self.__dataclass_fields__}  # type: ignore[attr-defined]
        data["petal_colors"] = list(self.petal_colors)
        return data


@dataclass(slots=True)
class SceneConfig:
    """Configuration complète d'une affiche."""

    name: str
    image: str | None
    text_zones: tuple[TextZone, ...]
    birds: tuple[BirdZone, ...] = ()
    flowers: tuple[FlowerZone, ...] = ()
    effects: EffectsConfig = field(default_factory=EffectsConfig)

    # -- (dé)sérialisation ---------------------------------------------------
    @classmethod
    def from_dict(cls, data: dict[str, Any], *, name: str = "sans_titre") -> "SceneConfig":
        text_raw = data.get("text_zones") or []
        if not text_raw:
            LOGGER.warning(
                "Aucune zone de texte déclarée : protection centrale par défaut appliquée. "
                "Déclarez 'text_zones' pour une garantie au pixel près."
            )
            text_raw = [{"rect": [0.12, 0.22, 0.76, 0.56], "label": "texte (défaut)"}]
        return cls(
            name=str(data.get("name", name)),
            image=data.get("image"),
            text_zones=tuple(TextZone.from_dict(z, i) for i, z in enumerate(text_raw)),
            birds=tuple(BirdZone.from_dict(b, i) for i, b in enumerate(data.get("birds") or [])),
            flowers=tuple(FlowerZone.from_dict(f, i) for i, f in enumerate(data.get("flowers") or [])),
            effects=EffectsConfig.from_dict(data.get("effects")),
        )

    @classmethod
    def from_json(cls, path: Path) -> "SceneConfig":
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON invalide dans {path} : {exc}") from exc
        return cls.from_dict(data, name=path.stem)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "image": self.image,
            "_coordonnees": "Toutes les coordonnées sont normalisées : 0.0 = haut/gauche, 1.0 = bas/droite.",
            "text_zones": [z.to_dict() for z in self.text_zones],
            "birds": [b.to_dict() for b in self.birds],
            "flowers": [f.to_dict() for f in self.flowers],
            "effects": self.effects.to_dict(),
        }

    def to_json(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")

    def resolve_image(self, config_path: Path, cli_image: Path | None) -> Path:
        """Détermine le chemin de l'image : CLI > champ 'image' du JSON."""
        if cli_image is not None:
            return cli_image
        if not self.image:
            raise ValueError(
                "Aucune image fournie : passez le chemin en argument ou renseignez "
                "le champ 'image' dans le JSON."
            )
        candidate = Path(self.image)
        return candidate if candidate.is_absolute() else (config_path.parent / candidate).resolve()


@dataclass(slots=True)
class RenderOptions:
    """Options de rendu vidéo."""

    duration: float = 6.0        # secondes (une boucle complète)
    fps: int = 30
    width: int = 0               # 0 = résolution native
    intensity: float = 1.0       # multiplicateur global des amplitudes
    gif_width: int = 420
    gif_step: int = 2            # 1 image GIF toutes les `gif_step` images vidéo

    @property
    def n_frames(self) -> int:
        return max(2, int(round(self.duration * self.fps)))


# ---------------------------------------------------------------------------
# Sprites d'oiseaux (détourage GrabCut + fond reconstruit)
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class Sprite:
    """Sujet détouré prêt à être recomposé à chaque image."""

    zone: BirdZone
    bgr: np.ndarray              # patch couleur (h, w, 3) uint8
    alpha: np.ndarray            # patch alpha (h, w) float32 0..1
    origin: tuple[int, int]      # (x, y) du patch dans l'image complète
    anchor: tuple[float, float]  # centre de transformation, coords du patch

    @property
    def pad(self) -> int:
        """Marge de sécurité pour rotation/dérive sans rognage."""
        return int(max(24, self.zone.amplitude_px * 2 + 16))


def _elliptical_falloff(w: int, h: int) -> np.ndarray:
    """Fondu elliptique doux : masque les éventuels coins rectangulaires."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rx, ry = w * 0.58, h * 0.58
    r = np.sqrt(((xx - w / 2) / rx) ** 2 + ((yy - h / 2) / ry) ** 2)
    return np.clip(1.25 - r, 0.0, 1.0).astype(np.float32)


def extract_sprite(
    img: np.ndarray, zone: BirdZone, forbidden_mask: np.ndarray | None = None
) -> Sprite:
    """Détoure un oiseau par GrabCut (repli elliptique si le résultat dégénère).

    Le rectangle GrabCut est resserré à 76 % de la boîte déclarée : les
    extrémités des ailes peuvent en dépasser légèrement, GrabCut les
    récupère via les classes probables ; le fondu elliptique final évite
    tout artefact rectangulaire lors des petits déplacements.

    ``forbidden_mask`` (masque du texte, image entière) : l'alpha y est forcé
    à zéro — un oiseau proche des lettres ne peut pas « embarquer » un
    fragment de calligraphie dans son sprite.
    """
    height, width = img.shape[:2]
    pad_ctx = 6
    x0, y0, x1, y1 = zone.bbox.to_pixels(width, height, expand_px=pad_ctx)
    crop = img[y0:y1, x0:x1].copy()
    ch, cw = crop.shape[:2]

    alpha = np.zeros((ch, cw), dtype=np.float32)
    ok = False
    try:
        mask = np.zeros((ch, cw), dtype=np.uint8)
        bgd = np.zeros((1, 65), dtype=np.float64)
        fgd = np.zeros((1, 65), dtype=np.float64)
        mx, my = int(cw * 0.12), int(ch * 0.12)
        rect = (mx, my, max(4, cw - 2 * mx), max(4, ch - 2 * my))
        cv2.grabCut(crop, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
        binary = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
        binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        coverage = float(np.mean(binary > 0))
        if 0.04 <= coverage <= 0.88:
            binary = cv2.erode(binary, np.ones((3, 3), np.uint8), iterations=1)
            alpha = cv2.GaussianBlur(binary.astype(np.float32) / 255.0, (5, 5), 0)
            ok = True
            LOGGER.debug("GrabCut %-22s couverture %.0f %%", zone.label, coverage * 100)
    except cv2.error as exc:  # pragma: no cover - dépend de l'image
        LOGGER.warning("GrabCut a échoué pour %s (%s) — repli elliptique.", zone.label, exc)

    if not ok:
        falloff = _elliptical_falloff(cw, ch)
        alpha = cv2.GaussianBlur((falloff > 0.35).astype(np.float32), (9, 9), 0)
    # Le fondu elliptique s'applique dans tous les cas (anti-coins), puis une
    # courbe de contraste resserre la frange semi-transparente : c'est elle
    # qui, sinon, laisse voir le fond reconstruit en halo autour de l'oiseau.
    alpha = np.clip(alpha * _elliptical_falloff(cw, ch), 0.0, 1.0)
    alpha = np.clip(alpha * 1.6 - 0.12, 0.0, 1.0)
    alpha = cv2.GaussianBlur(alpha, (3, 3), 0)
    # Jamais de pixels de texte dans un sprite.
    if forbidden_mask is not None:
        alpha[forbidden_mask[y0:y1, x0:x1]] = 0.0

    return Sprite(
        zone=zone,
        bgr=crop,
        alpha=alpha.astype(np.float32),
        origin=(x0, y0),
        anchor=(cw / 2.0, ch / 2.0),
    )


def build_clean_plate(img: np.ndarray, sprites: Sequence[Sprite]) -> np.ndarray:
    """Reconstruit le fond SANS les oiseaux (inpainting Telea).

    Quand un oiseau se déplace de quelques pixels, c'est ce fond « propre »
    qui apparaît derrière lui : pas de fantôme, pas de double contour.
    """
    if not sprites:
        return img.copy()
    height, width = img.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    for sp in sprites:
        x0, y0 = sp.origin
        h, w = sp.alpha.shape
        mask[y0 : y0 + h, x0 : x0 + w] = np.maximum(
            mask[y0 : y0 + h, x0 : x0 + w], (sp.alpha > 0.04).astype(np.uint8) * 255
        )
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)
    return cv2.inpaint(img, mask, 4, cv2.INPAINT_TELEA)


# ---------------------------------------------------------------------------
# Pétales dérivantes
# ---------------------------------------------------------------------------
@dataclass(slots=True)
class Petal:
    x0: float
    y0: float
    fall: float          # distance verticale parcourue sur une boucle
    sway: float
    phase: float
    offset: float        # position dans son cycle à t=0
    spin: int            # rotations complètes par boucle (entier ⇒ bouclable)
    scale: float
    bgr_patch: np.ndarray
    alpha_patch: np.ndarray


def _make_petal_patch(color_bgr: tuple[int, int, int], rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Petit pétale elliptique biseauté, rendu une seule fois puis réutilisé."""
    w, h = 26, 16
    alpha = np.zeros((h, w), dtype=np.float32)
    cv2.ellipse(alpha, (w // 2, h // 2), (w // 2 - 1, h // 2 - 1), 0, 0, 360, 1.0, -1)
    # Pointe du pétale : dégradé horizontal qui affine une extrémité.
    grad = np.tile(np.linspace(0.35, 1.0, w, dtype=np.float32), (h, 1))
    alpha = cv2.GaussianBlur(alpha * grad, (3, 3), 0)
    bgr = np.zeros((h, w, 3), dtype=np.uint8)
    tint = 0.9 + 0.2 * float(rng.random())
    bgr[:] = tuple(min(255, int(c * tint)) for c in color_bgr)
    # Veine centrale légèrement plus sombre.
    cv2.line(bgr, (2, h // 2), (w - 3, h // 2), tuple(int(c * 0.78) for c in color_bgr), 1)
    return bgr, alpha


# ---------------------------------------------------------------------------
# Moteur d'animation
# ---------------------------------------------------------------------------
class CalligraphyAnimator:
    """Génère les images animées d'une affiche, texte strictement préservé.

    Usage typique ::

        anim = CalligraphyAnimator(Path("affiche.jpg"), config, options)
        for frame in anim.frames():
            ...  # frame BGR uint8, texte bit-à-bit identique à la source
    """

    #: Échelle du champ de déplacement : calculé en basse résolution (×16 plus
    #: rapide) puis sur-échantillonné — le vent est par nature basse fréquence.
    FLOW_SCALE = 0.25

    def __init__(self, image_path: Path, config: SceneConfig, options: RenderOptions) -> None:
        self.image_path = image_path
        self.config = config
        self.options = options
        self.original = imread_unicode(image_path)
        self.height, self.width = self.original.shape[:2]
        LOGGER.info("Image %s : %d×%d", image_path.name, self.width, self.height)

        self._build_protection_masks()
        self._prepare_sprites()
        self._prepare_flow_field()
        self._prepare_gold_mask()
        self._prepare_petals()

    # -- Préparation (une seule fois) ---------------------------------------
    def _build_protection_masks(self) -> None:
        """Construit le « sanctuaire » : cœur == 1.0 strict, fondu à l'extérieur."""
        fx = self.config.effects
        core = np.zeros((self.height, self.width), dtype=np.uint8)
        for zone in self.config.text_zones:
            x0, y0, x1, y1 = zone.rect.to_pixels(
                self.width, self.height, expand_px=fx.protect_margin_px
            )
            core[y0:y1, x0:x1] = 255
        self.core_mask = core > 0

        feather = max(2, fx.protect_feather_px)
        ksize = feather * 2 + 1
        alpha = cv2.GaussianBlur(core.astype(np.float32) / 255.0, (ksize, ksize), 0)
        alpha[self.core_mask] = 1.0          # ← la garantie : cœur strictement figé
        self.protect_alpha = np.clip(alpha, 0.0, 1.0).astype(np.float32)

        # Zone tampon élargie où TOUS les effets sont éteints progressivement.
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (41, 41))
        dilated = cv2.dilate(core, k)
        gate = cv2.GaussianBlur(dilated.astype(np.float32) / 255.0, (31, 31), 0)
        gate[self.core_mask] = 1.0
        self.effect_gate = (1.0 - np.clip(gate, 0.0, 1.0)).astype(np.float32)

    @property
    def bird_engine(self) -> str:
        engine = str(self.config.effects.bird_engine).lower()
        if engine not in {"warp", "sprite"}:
            raise ValueError(f"bird_engine invalide : {engine!r} (attendu : warp | sprite)")
        return engine

    def _prepare_sprites(self) -> None:
        """Moteur « sprite » uniquement ; en « warp », la plaque = l'original."""
        if self.config.effects.birds and self.config.birds and self.bird_engine == "sprite":
            t0 = time.perf_counter()
            self.sprites = [
                extract_sprite(self.original, z, forbidden_mask=self.core_mask)
                for z in self.config.birds
            ]
            LOGGER.info(
                "Détourage : %d sujet(s) en %.1f s", len(self.sprites), time.perf_counter() - t0
            )
        else:
            self.sprites = []
            if self.config.effects.birds and self.config.birds:
                LOGGER.info("Oiseaux : moteur 'warp' (déformation locale, sans détourage)")
        self.plate = build_clean_plate(self.original, self.sprites)

    def _prepare_flow_field(self) -> None:
        """Pré-calcule (en basse résolution) les pondérations du vent floral."""
        w, h = self.width, self.height
        lw, lh = max(8, int(w * self.FLOW_SCALE)), max(8, int(h * self.FLOW_SCALE))
        self._lw, self._lh = lw, lh
        xs = (np.arange(lw, dtype=np.float32) + 0.5) / self.FLOW_SCALE
        ys = (np.arange(lh, dtype=np.float32) + 0.5) / self.FLOW_SCALE
        lx, ly = np.meshgrid(xs, ys)
        self._x_norm = (lx / w).astype(np.float32)
        self._y_norm = (ly / h).astype(np.float32)
        self._diag = ((lx + ly) / (w + h)).astype(np.float32)

        gate_low = cv2.resize(self.effect_gate, (lw, lh), interpolation=cv2.INTER_AREA)

        # Pondération « végétation de bordure » pour la brise globale.
        small = cv2.resize(self.plate, (lw, lh), interpolation=cv2.INTER_AREA)
        sat = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)[:, :, 1].astype(np.float32) / 255.0
        dist_edge = np.minimum(np.minimum(lx, w - lx), np.minimum(ly, h - ly))
        border_w = 1.0 - np.clip(dist_edge / (0.30 * min(w, h)), 0.0, 1.0)
        self._wind_weight = (np.clip(0.30 + 0.70 * sat, 0, 1) * border_w * gate_low).astype(np.float32)

        # Une gaussienne par fleur (+ ses moments radiaux pour la « respiration »).
        self._flower_terms: list[tuple[FlowerZone, np.ndarray, np.ndarray, np.ndarray]] = []
        for zone in self.config.flowers:
            cx, cy = zone.cx * w, zone.cy * h
            sigma = max(6.0, 0.55 * zone.radius * w)
            g = np.exp(-((lx - cx) ** 2 + (ly - cy) ** 2) / (2.0 * sigma**2))
            g[g < 0.01] = 0.0
            g *= gate_low
            self._flower_terms.append(
                (zone, g.astype(np.float32), ((lx - cx) * g).astype(np.float32), ((ly - cy) * g).astype(np.float32))
            )

        # Moteur « warp » : une gaussienne ELLIPTIQUE par oiseau (calée sur sa
        # boîte) — l'oiseau et son voisinage immédiat bougent d'un seul tenant,
        # le fond s'étire de quelques pixels sans aucune couture visible.
        self._bird_terms: list[tuple[BirdZone, np.ndarray, np.ndarray, np.ndarray]] = []
        if self.bird_engine == "warp":
            for zone in self.config.birds:
                cx = (zone.bbox.x + zone.bbox.w / 2) * w
                cy = (zone.bbox.y + zone.bbox.h / 2) * h
                sx = max(8.0, 0.42 * zone.bbox.w * w)
                sy = max(8.0, 0.42 * zone.bbox.h * h)
                g = np.exp(-0.5 * (((lx - cx) / sx) ** 2 + ((ly - cy) / sy) ** 2))
                g[g < 0.01] = 0.0
                g *= gate_low
                self._bird_terms.append(
                    (zone, g.astype(np.float32), ((lx - cx) * g).astype(np.float32), ((ly - cy) * g).astype(np.float32))
                )

        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self._base_x, self._base_y = xx, yy

    def _prepare_gold_mask(self) -> None:
        """Masque des pixels dorés (HSV) pour le scintillement des ornements."""
        hsv = cv2.cvtColor(self.plate, cv2.COLOR_BGR2HSV)
        gold = cv2.inRange(hsv, np.array([14, 65, 85]), np.array([36, 255, 255]))
        gold = cv2.GaussianBlur(gold.astype(np.float32) / 255.0, (7, 7), 0)
        self._gold = (gold * (1.0 - self.protect_alpha)).astype(np.float32)

    def _prepare_petals(self) -> None:
        fx = self.config.effects
        self._petals: list[Petal] = []
        if not (fx.petals and fx.petal_count > 0):
            return
        rng = np.random.default_rng(fx.seed)
        w, h = self.width, self.height
        patches = [_make_petal_patch(hex_to_bgr(c), rng) for c in fx.petal_colors]

        attempts = 0
        while len(self._petals) < fx.petal_count and attempts < fx.petal_count * 300:
            attempts += 1
            # Naissance dans les colonnes latérales (70 %) ou la frise du bas
            # (30 %) : jamais au-dessus du texte, pour ne pas « disparaître »
            # derrière le sanctuaire en tombant.
            if rng.random() < 0.7:
                x = float(rng.uniform(0.01, 0.19) if rng.random() < 0.5 else rng.uniform(0.81, 0.99)) * w
                y = float(rng.uniform(0.02, 0.92)) * h
            else:
                x = float(rng.uniform(0.02, 0.98)) * w
                y = float(rng.uniform(0.80, 0.95)) * h
            fall = float(rng.uniform(70, 190))
            # Toute la trajectoire doit rester hors de la zone tampon du texte.
            ok = True
            for yy in np.linspace(y, min(h - 2, y + fall), 8):
                if self.effect_gate[int(yy), int(x)] < 0.92:
                    ok = False
                    break
            if not ok:
                continue
            bgr_patch, alpha_patch = patches[int(rng.integers(len(patches)))]
            self._petals.append(
                Petal(
                    x0=x,
                    y0=y,
                    fall=fall,
                    sway=float(rng.uniform(8, 22)),
                    phase=float(rng.random()),
                    offset=float(rng.random()),
                    spin=int(rng.choice([-2, -1, 1, 2])),
                    scale=float(rng.uniform(0.65, 1.25)),
                    bgr_patch=bgr_patch,
                    alpha_patch=alpha_patch,
                )
            )
        LOGGER.info("Pétales : %d particule(s) confinées aux bordures", len(self._petals))

    # -- Cinématique d'un oiseau (partagée par les deux moteurs) --------------
    def _bird_kinematics(self, zone: BirdZone, t: float) -> tuple[float, float, float, float, float]:
        """Retourne (dx, dy, sx, sy, rotation_deg) de l'oiseau au temps ``t``.

        Toutes les fréquences sont entières par boucle ⇒ bouclage parfait.
        """
        opt, ph = self.options, zone.phase
        match zone.mode:
            case BirdMode.PERCHED:
                amp_x, amp_y = 1.6, 1.2
                rot = 0.7 * float(osc(t, 2, ph))
                sx = sy = 1.0 + 0.007 * float(osc(t, 2, ph + 0.3))   # respiration
            case BirdMode.BUTTERFLY:
                amp_x, amp_y = zone.amplitude_px, zone.amplitude_px * 0.8
                rot = zone.rotation_deg * float(osc(t, 1, ph + 0.15))
                fl = float(osc(t, zone.flutter_cycles, ph))
                sx = 1.0 - 1.5 * zone.flutter * abs(fl)               # ailes qui se referment
                sy = 1.0 + 0.30 * zone.flutter * fl
            case _:  # HOVER
                amp_x, amp_y = zone.amplitude_px, zone.amplitude_px * 0.7
                rot = zone.rotation_deg * float(osc(t, 1, ph + 0.15))
                fl = float(osc(t, zone.flutter_cycles, ph))
                sy = 1.0 + zone.flutter * fl                          # battement vertical
                sx = 1.0 - 0.35 * zone.flutter * fl                   # conservation du « volume »
        dx = amp_x * opt.intensity * float(osc(t, 1, ph))
        dy = amp_y * opt.intensity * float(osc(t, zone.bob_cycles, ph + 0.3))
        return dx, dy, sx, sy, rot

    # -- Étapes du pipeline par image ----------------------------------------
    def _warp_scene(self, t: float) -> np.ndarray:
        """Vent floral + (moteur warp) oiseaux : UNE seule déformation remap."""
        fx, opt = self.config.effects, self.options
        warp_birds = fx.birds and self.bird_engine == "warp" and bool(self._bird_terms)
        if not fx.flowers and not warp_birds:
            return self.plate.copy()

        dx = np.zeros((self._lh, self._lw), dtype=np.float32)
        dy = np.zeros_like(dx)

        if fx.flowers:
            # Brise globale sur la végétation des bordures.
            wind = fx.wind_px * opt.intensity
            dx += wind * self._wind_weight * osc(t + 0.7 * self._y_norm + 0.25 * self._x_norm, 1, 0.0)
            dy += wind * 0.4 * self._wind_weight * osc(t + 0.6 * self._x_norm, 1, 0.25)

            # Balancement + respiration de chaque fleur déclarée.
            for zone, g, rel_x, rel_y in self._flower_terms:
                sway_x = zone.sway_px * opt.intensity * float(osc(t, zone.cycles, zone.phase))
                sway_y = zone.sway_px * 0.45 * opt.intensity * float(osc(t, zone.cycles, zone.phase + 0.18))
                breathe = zone.breathe * float(osc(t, zone.cycles, zone.phase + 0.10))
                dx += g * sway_x + rel_x * breathe
                dy += g * sway_y + rel_y * breathe

        if warp_birds:
            # Chaque oiseau : translation + compression (battement) + rotation,
            # appliquées comme champ de déplacement local pondéré par sa gaussienne.
            for zone, g, rel_x, rel_y in self._bird_terms:
                bdx, bdy, sx, sy, rot = self._bird_kinematics(zone, t)
                theta = math.radians(rot)
                dx += g * bdx + rel_x * (sx - 1.0) - rel_y * theta
                dy += g * bdy + rel_y * (sy - 1.0) + rel_x * theta

        dx_full = cv2.resize(dx, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        dy_full = cv2.resize(dy, (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        return cv2.remap(
            self.plate,
            (self._base_x - dx_full).astype(np.float32),
            (self._base_y - dy_full).astype(np.float32),
            interpolation=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REFLECT,
        )

    def _add_shimmer(self, frame: np.ndarray, t: float) -> np.ndarray:
        """Vague de lumière diagonale sur les dorures (hors texte)."""
        if not self.config.effects.shimmer:
            return frame
        shine_low = np.clip(osc(self._diag * 2.2 - t, 1, 0.0), 0.0, 1.0) ** 3
        shine = cv2.resize(shine_low.astype(np.float32), (self.width, self.height), interpolation=cv2.INTER_CUBIC)
        glow = (shine * self._gold)[..., None] * np.array([10.0, 26.0, 42.0], dtype=np.float32)  # BGR chaud
        return np.clip(frame.astype(np.float32) + glow, 0, 255).astype(np.uint8)

    @staticmethod
    def _blend(canvas: np.ndarray, patch: np.ndarray, alpha: np.ndarray, x0: int, y0: int) -> None:
        """Composition alpha d'un patch sur le canevas, avec rognage aux bords."""
        h_c, w_c = canvas.shape[:2]
        h_p, w_p = patch.shape[:2]
        x1, y1 = x0 + w_p, y0 + h_p
        cx0, cy0 = max(0, x0), max(0, y0)
        cx1, cy1 = min(w_c, x1), min(h_c, y1)
        if cx0 >= cx1 or cy0 >= cy1:
            return
        sub_patch = patch[cy0 - y0 : cy1 - y0, cx0 - x0 : cx1 - x0].astype(np.float32)
        sub_alpha = alpha[cy0 - y0 : cy1 - y0, cx0 - x0 : cx1 - x0][..., None]
        roi = canvas[cy0:cy1, cx0:cx1]
        canvas[cy0:cy1, cx0:cx1] = np.clip(
            roi.astype(np.float32) * (1.0 - sub_alpha) + sub_patch * sub_alpha, 0, 255
        ).astype(np.uint8)

    def _bird_transform(self, sprite: Sprite, t: float) -> tuple[np.ndarray, np.ndarray, int, int]:
        """Moteur « sprite » : patch détouré transformé (dérive/rotation/battement)."""
        dx, dy, sx, sy, rot = self._bird_kinematics(sprite.zone, t)

        pad = sprite.pad
        ax, ay = sprite.anchor
        ang = math.radians(rot)
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        # M = T(ancre + dérive + pad) · R(θ) · S(sx, sy) · T(−ancre)
        m = np.array(
            [
                [cos_a * sx, -sin_a * sy, ax + dx + pad - (cos_a * sx * ax - sin_a * sy * ay)],
                [sin_a * sx, cos_a * sy, ay + dy + pad - (sin_a * sx * ax + cos_a * sy * ay)],
            ],
            dtype=np.float32,
        )
        h, w = sprite.bgr.shape[:2]
        dst = (w + 2 * pad, h + 2 * pad)
        warped_bgr = cv2.warpAffine(sprite.bgr, m, dst, flags=cv2.INTER_LINEAR, borderValue=0)
        warped_alpha = cv2.warpAffine(sprite.alpha, m, dst, flags=cv2.INTER_LINEAR, borderValue=0)
        return warped_bgr, warped_alpha, sprite.origin[0] - pad, sprite.origin[1] - pad

    def _draw_petals(self, frame: np.ndarray, t: float) -> None:
        """Pétales dérivantes : fondu sinusoïdal, invisibles près du texte."""
        for petal in self._petals:
            p = (t + petal.offset) % 1.0
            opacity = float(np.sin(math.pi * p) ** 1.5) * 0.60
            if opacity <= 0.01:
                continue
            x = petal.x0 + petal.sway * float(osc(p, 2, petal.phase))
            y = petal.y0 + petal.fall * p
            xi, yi = int(round(x)), int(round(y))
            if not (0 <= xi < self.width and 0 <= yi < self.height):
                continue
            opacity *= float(self.effect_gate[yi, xi])  # s'éteint près du texte
            if opacity <= 0.01:
                continue
            angle = 360.0 * petal.spin * p + 180.0 * petal.phase
            size = 44
            m = cv2.getRotationMatrix2D((13, 8), angle, petal.scale)
            m[0, 2] += size / 2 - 13
            m[1, 2] += size / 2 - 8
            patch = cv2.warpAffine(petal.bgr_patch, m, (size, size), flags=cv2.INTER_LINEAR, borderValue=0)
            alpha = cv2.warpAffine(petal.alpha_patch, m, (size, size), flags=cv2.INTER_LINEAR, borderValue=0)
            self._blend(frame, patch, np.clip(alpha * opacity, 0, 1), xi - size // 2, yi - size // 2)

    # -- Image complète -------------------------------------------------------
    def render_frame(self, t: float) -> np.ndarray:
        """Rend l'image au temps normalisé ``t`` ∈ [0, 1] (0 = début de boucle).

        Garantie : dans le cœur des zones de texte, le résultat est
        **strictement identique** à l'image d'origine, au bit près.
        """
        frame = self._warp_scene(t)
        frame = self._add_shimmer(frame, t)

        if self.config.effects.birds and self.bird_engine == "sprite":
            for sprite in self.sprites:
                patch, alpha, x0, y0 = self._bird_transform(sprite, t)
                self._blend(frame, patch, alpha, x0, y0)

        self._draw_petals(frame, t)

        # ── Restauration du sanctuaire (TOUJOURS en dernier) ────────────────
        a = self.protect_alpha[..., None]
        frame = np.clip(frame.astype(np.float32) * (1.0 - a) + self.original.astype(np.float32) * a, 0, 255)
        frame = frame.astype(np.uint8)
        frame[self.core_mask] = self.original[self.core_mask]  # ceinture et bretelles
        return frame

    def frames(self) -> Iterator[np.ndarray]:
        """Itère sur les images de la boucle (t = 0 incluse, t = 1 exclue)."""
        n = self.options.n_frames
        for i in range(n):
            yield self.render_frame(i / n)

    # -- Vérifications --------------------------------------------------------
    def verify_text_integrity(self, samples: int = 24) -> dict[str, Any]:
        """Prouve que le texte n'a pas bougé d'un bit sur ``samples`` images.

        Retourne aussi l'écart de bouclage (image t=0 vs t=1) : il doit être
        quasi nul pour une boucle parfaite. Attention : cette vérification
        porte sur les images AVANT encodage ; un MP4 (pertes H.264) modifiera
        forcément les valeurs, mais le texte n'y est ni déplacé ni déformé.
        Pour un livrable strictement sans perte, utilisez le format ``png``.
        """
        max_diff = 0
        for i in range(samples):
            frame = self.render_frame(i / samples)
            diff = np.abs(frame.astype(np.int16) - self.original.astype(np.int16))
            max_diff = max(max_diff, int(diff[self.core_mask].max(initial=0)))
        first, wrapped = self.render_frame(0.0), self.render_frame(1.0)
        loop_mae = float(np.mean(np.abs(first.astype(np.float32) - wrapped.astype(np.float32))))
        # Les ornements, eux, doivent bel et bien bouger :
        mid = self.render_frame(0.5)
        outside = ~cv2.dilate(self.core_mask.astype(np.uint8), np.ones((25, 25), np.uint8)).astype(bool)
        motion_mae = float(
            np.mean(np.abs(mid.astype(np.float32) - self.original.astype(np.float32))[outside])
        )
        report = {
            "echantillons": samples,
            "ecart_max_dans_le_texte": max_diff,
            "texte_intact": max_diff == 0,
            "erreur_moyenne_bouclage_t0_vs_t1": round(loop_mae, 3),
            "mouvement_moyen_ornements": round(motion_mae, 3),
        }
        LOGGER.info("Vérification : %s", report)
        return report


# ---------------------------------------------------------------------------
# Sorties vidéo / GIF / séquence PNG
# ---------------------------------------------------------------------------
class OutputSink:
    """Écrit simultanément MP4 (H.264 si possible), GIF et/ou PNG sans perte."""

    def __init__(
        self,
        *,
        mp4_path: Path | None,
        gif_path: Path | None,
        png_dir: Path | None,
        fps: int,
        size: tuple[int, int],
        gif_width: int,
        gif_step: int,
    ) -> None:
        self.mp4_path, self.gif_path, self.png_dir = mp4_path, gif_path, png_dir
        self.fps, self.size = fps, size
        self.gif_step = max(1, gif_step)
        self._frame_idx = 0
        self._mp4_writer: Any = None
        self._gif_writer: Any = None
        self._imageio = self._try_import_imageio()

        w, h = size
        self.gif_size = (
            even(min(gif_width, w)),
            even(max(2, int(h * min(gif_width, w) / w))),
        )
        if png_dir is not None:
            png_dir.mkdir(parents=True, exist_ok=True)
        if mp4_path is not None:
            mp4_path.parent.mkdir(parents=True, exist_ok=True)
            self._open_mp4(mp4_path)
        if gif_path is not None:
            gif_path.parent.mkdir(parents=True, exist_ok=True)
            if self._imageio is None:
                LOGGER.warning("imageio absent : GIF ignoré (pip install imageio).")
            else:
                self._gif_writer = self._imageio.get_writer(
                    str(gif_path), mode="I", fps=max(1, fps // self.gif_step), loop=0
                )

    @staticmethod
    def _try_import_imageio() -> Any:
        try:
            import imageio.v2 as imageio

            return imageio
        except ImportError:
            return None

    def _open_mp4(self, path: Path) -> None:
        w, h = self.size
        if self._imageio is not None:
            try:
                self._mp4_writer = self._imageio.get_writer(
                    str(path), fps=self.fps, codec="libx264", quality=8,
                    pixelformat="yuv420p", macro_block_size=None,
                )
                self._mp4_is_imageio = True
                return
            except Exception as exc:  # ffmpeg absent, etc.
                LOGGER.warning("imageio-ffmpeg indisponible (%s) — repli OpenCV mp4v.", exc)
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(str(path), fourcc, self.fps, (w, h))
        if not writer.isOpened():
            raise IOError(f"Impossible d'ouvrir le fichier vidéo : {path}")
        self._mp4_writer = writer
        self._mp4_is_imageio = False

    def write(self, frame_bgr: np.ndarray) -> None:
        w, h = self.size
        if frame_bgr.shape[1] != w or frame_bgr.shape[0] != h:
            frame_bgr = cv2.resize(frame_bgr, (w, h), interpolation=cv2.INTER_AREA)
        if self._mp4_writer is not None:
            if self._mp4_is_imageio:
                self._mp4_writer.append_data(cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB))
            else:
                self._mp4_writer.write(frame_bgr)
        if self._gif_writer is not None and self._frame_idx % self.gif_step == 0:
            small = cv2.resize(frame_bgr, self.gif_size, interpolation=cv2.INTER_AREA)
            self._gif_writer.append_data(cv2.cvtColor(small, cv2.COLOR_BGR2RGB))
        if self.png_dir is not None:
            imwrite_unicode(self.png_dir / f"frame_{self._frame_idx:04d}.png", frame_bgr)
        self._frame_idx += 1

    def close(self) -> None:
        if self._mp4_writer is not None:
            if self._mp4_is_imageio:
                self._mp4_writer.close()
            else:
                self._mp4_writer.release()
            LOGGER.info("MP4 écrit : %s", self.mp4_path)
        if self._gif_writer is not None:
            self._gif_writer.close()
            LOGGER.info("GIF écrit : %s", self.gif_path)
        if self.png_dir is not None:
            LOGGER.info("Séquence PNG (sans perte) : %s (%d images)", self.png_dir, self._frame_idx)

    def __enter__(self) -> "OutputSink":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


def output_size(native_w: int, native_h: int, requested_width: int) -> tuple[int, int]:
    if requested_width and requested_width < native_w:
        return even(requested_width), even(int(native_h * requested_width / native_w))
    return even(native_w), even(native_h)


# ---------------------------------------------------------------------------
# Aperçu annoté (indispensable pour régler les zones d'une nouvelle image)
# ---------------------------------------------------------------------------
def render_preview(image_path: Path, config: SceneConfig, out_path: Path) -> Path:
    img = imread_unicode(image_path)
    h, w = img.shape[:2]
    overlay = img.copy()
    fx = config.effects

    for zone in config.text_zones:  # rouge = sanctuaire intouchable
        x0, y0, x1, y1 = zone.rect.to_pixels(w, h, expand_px=fx.protect_margin_px)
        cv2.rectangle(overlay, (x0, y0), (x1, y1), (0, 0, 255), -1)
        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 0, 255), 2)
        cv2.putText(img, f"TEXTE protege: {zone.label}", (x0 + 4, max(14, y0 - 6)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1, cv2.LINE_AA)
    img = cv2.addWeighted(overlay, 0.18, img, 0.82, 0)

    for bird in config.birds:  # vert = oiseaux
        x0, y0, x1, y1 = bird.bbox.to_pixels(w, h)
        cv2.rectangle(img, (x0, y0), (x1, y1), (0, 200, 0), 2)
        cv2.putText(img, f"{bird.mode.value}: {bird.label}", (x0 + 3, y1 - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 160, 0), 1, cv2.LINE_AA)

    for flower in config.flowers:  # magenta = fleurs
        cx, cy = int(flower.cx * w), int(flower.cy * h)
        r = int(flower.radius * w)
        cv2.circle(img, (cx, cy), r, (255, 0, 200), 2)
        cv2.circle(img, (cx, cy), 3, (255, 0, 200), -1)
        cv2.putText(img, flower.label, (cx + 5, cy - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 0, 160), 1, cv2.LINE_AA)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    imwrite_unicode(out_path, img)
    LOGGER.info("Aperçu annoté : %s", out_path)
    return out_path


# ---------------------------------------------------------------------------
# Commandes
# ---------------------------------------------------------------------------
def cmd_render(
    image_path: Path,
    config: SceneConfig,
    options: RenderOptions,
    *,
    out_mp4: Path | None,
    out_gif: Path | None,
    out_png_dir: Path | None,
    verify: bool,
) -> dict[str, Any] | None:
    animator = CalligraphyAnimator(image_path, config, options)
    size = output_size(animator.width, animator.height, options.width)
    total = options.n_frames
    LOGGER.info(
        "Rendu %s : %d images, %.1f s @ %d i/s, sortie %d×%d",
        config.name, total, options.duration, options.fps, *size,
    )
    t0 = time.perf_counter()
    with OutputSink(
        mp4_path=out_mp4, gif_path=out_gif, png_dir=out_png_dir,
        fps=options.fps, size=size, gif_width=options.gif_width, gif_step=options.gif_step,
    ) as sink:
        for i, frame in enumerate(animator.frames()):
            sink.write(frame)
            if (i + 1) % max(1, total // 10) == 0 or i + 1 == total:
                LOGGER.info("  … %d/%d images (%.0f %%)", i + 1, total, 100 * (i + 1) / total)
    LOGGER.info("Rendu terminé en %.1f s", time.perf_counter() - t0)
    return animator.verify_text_integrity() if verify else None


def default_config_for(image_path: Path) -> SceneConfig:
    """Modèle de départ pour une nouvelle affiche (à affiner via `preview`)."""
    return SceneConfig(
        name=image_path.stem,
        image=image_path.name,
        text_zones=(
            TextZone(NormRect(0.14, 0.30, 0.72, 0.16), "ligne 1 — AJUSTER"),
            TextZone(NormRect(0.14, 0.48, 0.72, 0.16), "ligne 2 — AJUSTER"),
        ),
        birds=(BirdZone(NormRect(0.10, 0.08, 0.18, 0.12), BirdMode.HOVER, "oiseau — EXEMPLE"),),
        flowers=(
            FlowerZone(0.12, 0.12, 0.07, "fleur — EXEMPLE"),
            FlowerZone(0.88, 0.85, 0.07, "fleur — EXEMPLE"),
        ),
    )


def find_config(image_path: Path, explicit: Path | None) -> SceneConfig:
    """Cherche la configuration : --config, sinon configs/<nom>.json, sinon défaut."""
    if explicit is not None:
        return SceneConfig.from_json(explicit)
    candidates = [
        image_path.parent / f"{image_path.stem}.json",
        image_path.parent.parent / "configs" / f"{image_path.stem}.json",
        Path(__file__).resolve().parent / "configs" / f"{image_path.stem}.json",
    ]
    for candidate in candidates:
        if candidate.is_file():
            LOGGER.info("Configuration trouvée : %s", candidate)
            return SceneConfig.from_json(candidate)
    LOGGER.warning(
        "Aucune configuration pour %s : modèle par défaut. Utilisez `init-config` "
        "puis `preview` pour déclarer précisément texte, oiseaux et fleurs.",
        image_path.name,
    )
    return default_config_for(image_path)


def apply_cli_effects(config: SceneConfig, args: argparse.Namespace) -> SceneConfig:
    """Les drapeaux --birds/--no-birds… (None = inchangé) priment sur le JSON."""
    fx = config.effects
    overrides: dict[str, Any] = {}
    for attr in ("birds", "flowers", "shimmer", "petals"):
        value = getattr(args, attr, None)
        if value is not None:
            overrides[attr] = bool(value)
    engine = getattr(args, "bird_engine", None)
    if engine:
        overrides["bird_engine"] = str(engine)
    if overrides:
        return replace(config, effects=replace(fx, **overrides))
    return config


def build_options(args: argparse.Namespace) -> RenderOptions:
    return RenderOptions(
        duration=float(args.duration),
        fps=int(args.fps),
        width=int(args.width),
        intensity=float(args.intensity),
        gif_width=int(args.gif_width),
        gif_step=int(args.gif_step),
    )


# ---------------------------------------------------------------------------
# Interface en ligne de commande
# ---------------------------------------------------------------------------
def add_render_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--duration", type=float, default=6.0, help="durée d'une boucle, en secondes (défaut : 6)")
    parser.add_argument("--fps", type=int, default=30, help="images par seconde (défaut : 30)")
    parser.add_argument("--width", type=int, default=0, help="largeur de sortie, 0 = native")
    parser.add_argument("--intensity", type=float, default=1.0, help="multiplicateur des amplitudes (0.5 = subtil, 1.5 = marqué)")
    parser.add_argument("--gif-width", type=int, default=420, help="largeur du GIF")
    parser.add_argument("--gif-step", type=int, default=2, help="1 image GIF toutes les N images")
    parser.add_argument("--birds", action=argparse.BooleanOptionalAction, default=None, help="activer/couper les oiseaux")
    parser.add_argument("--bird-engine", choices=("warp", "sprite"), default=None, help="warp = déformation locale sans halo (défaut) ; sprite = détourage GrabCut")
    parser.add_argument("--flowers", action=argparse.BooleanOptionalAction, default=None, help="activer/couper le vent floral")
    parser.add_argument("--shimmer", action=argparse.BooleanOptionalAction, default=None, help="activer/couper le scintillement des dorures")
    parser.add_argument("--petals", action=argparse.BooleanOptionalAction, default=None, help="activer/couper les pétales")
    parser.add_argument("--verify", action="store_true", help="prouver après rendu que le texte est intact (bit à bit)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="animate_calligraphy.py",
        description="Anime oiseaux et fleurs des affiches de calligraphie — sans jamais toucher au texte.",
        epilog="Exemple : %(prog)s render images/03_creme_bordeaux.jpg --config configs/03_creme_bordeaux.json --verify",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("-v", "--verbose", action="store_true", help="journaux détaillés (DEBUG)")
    sub = parser.add_subparsers(dest="command", required=True)

    p_render = sub.add_parser("render", help="rendre UNE affiche en MP4 / GIF / PNG")
    p_render.add_argument("image", type=Path, help="image source (.jpg / .png)")
    p_render.add_argument("--config", type=Path, default=None, help="fichier JSON de zones (défaut : configs/<nom>.json)")
    p_render.add_argument("--output", type=Path, default=None, help="MP4 de sortie (défaut : output/<nom>_anime.mp4)")
    p_render.add_argument("--gif", type=Path, default=None, help="GIF de sortie (défaut : à côté du MP4)")
    p_render.add_argument("--no-gif", action="store_true", help="ne pas produire de GIF")
    p_render.add_argument("--png-dir", type=Path, default=None, help="dossier de séquence PNG SANS PERTE (texte garanti bit à bit)")
    add_render_arguments(p_render)

    p_batch = sub.add_parser("batch", help="rendre TOUTES les affiches décrites par un dossier de configs")
    p_batch.add_argument("--configs", type=Path, default=Path("configs"), help="dossier des JSON")
    p_batch.add_argument("--output-dir", type=Path, default=Path("output"), help="dossier de sortie")
    p_batch.add_argument("--no-gif", action="store_true", help="ne pas produire de GIF")
    add_render_arguments(p_batch)

    p_prev = sub.add_parser("preview", help="dessiner les zones sur l'image pour les régler")
    p_prev.add_argument("image", type=Path)
    p_prev.add_argument("--config", type=Path, default=None)
    p_prev.add_argument("--output", type=Path, default=None, help="défaut : output/<nom>_zones.jpg")

    p_init = sub.add_parser("init-config", help="créer un modèle de configuration pour une nouvelle image")
    p_init.add_argument("image", type=Path)
    p_init.add_argument("--output", type=Path, default=None, help="défaut : configs/<nom>.json")
    p_init.add_argument("--force", action="store_true", help="écraser si le fichier existe")

    p_ver = sub.add_parser("verify", help="vérifier l'intégrité du texte sans rendre de vidéo")
    p_ver.add_argument("image", type=Path)
    p_ver.add_argument("--config", type=Path, default=None)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(message)s",
        datefmt="%H:%M:%S",
    )

    try:
        match args.command:
            case "render":
                config = apply_cli_effects(find_config(args.image, args.config), args)
                out_mp4 = args.output or Path("output") / f"{args.image.stem}_anime.mp4"
                out_gif = None if args.no_gif else (args.gif or out_mp4.with_suffix(".gif"))
                cmd_render(
                    args.image, config, build_options(args),
                    out_mp4=out_mp4, out_gif=out_gif, out_png_dir=args.png_dir, verify=args.verify,
                )

            case "batch":
                json_files = sorted(args.configs.glob("*.json"))
                if not json_files:
                    raise FileNotFoundError(f"Aucun JSON dans {args.configs}")
                failures = 0
                for json_path in json_files:
                    try:
                        config = apply_cli_effects(SceneConfig.from_json(json_path), args)
                        image_path = config.resolve_image(json_path, None)
                        stem = image_path.stem
                        cmd_render(
                            image_path, config, build_options(args),
                            out_mp4=args.output_dir / f"{stem}_anime.mp4",
                            out_gif=None if args.no_gif else args.output_dir / f"{stem}_anime.gif",
                            out_png_dir=None, verify=args.verify,
                        )
                    except Exception as exc:  # on continue avec les autres affiches
                        failures += 1
                        LOGGER.error("Échec pour %s : %s", json_path.name, exc)
                LOGGER.info("Lot terminé : %d/%d réussite(s)", len(json_files) - failures, len(json_files))
                if failures:
                    return 1

            case "preview":
                config = find_config(args.image, args.config)
                out = args.output or Path("output") / f"{args.image.stem}_zones.jpg"
                render_preview(args.image, config, out)

            case "init-config":
                out = args.output or Path("configs") / f"{args.image.stem}.json"
                if out.exists() and not args.force:
                    raise FileExistsError(f"{out} existe déjà (--force pour écraser)")
                cfg = default_config_for(args.image)
                try:
                    rel = args.image.resolve().relative_to(out.parent.resolve())
                    cfg.image = rel.as_posix()
                except ValueError:
                    cfg.image = str(args.image)
                cfg.to_json(out)
                LOGGER.info("Modèle créé : %s — ajustez les zones puis lancez `preview`.", out)

            case "verify":
                config = find_config(args.image, args.config)
                animator = CalligraphyAnimator(args.image, config, RenderOptions())
                report = animator.verify_text_integrity()
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 0 if report["texte_intact"] else 1

    except (FileNotFoundError, FileExistsError, ValueError, IOError) as exc:
        LOGGER.error("%s", exc)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
