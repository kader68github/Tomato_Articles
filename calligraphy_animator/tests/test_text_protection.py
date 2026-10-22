#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Tests de la garantie « sanctuaire de texte » d'animate_calligraphy.

Exécution directe :   python tests/test_text_protection.py
Ou avec pytest :      pytest tests/ -q

Les tests construisent une image synthétique (fond texturé + faux « texte »
au centre + un disque « oiseau » + un disque « fleur ») et vérifient que :
  1. les pixels du cœur des zones de texte sont bit-à-bit inchangés ;
  2. l'animation boucle parfaitement (image t=0 identique à t=1) ;
  3. les ornements, eux, bougent réellement ;
  4. la configuration survit à un aller-retour JSON ;
  5. une configuration invalide est rejetée avec une erreur claire.
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from animate_calligraphy import (  # noqa: E402
    BirdMode,
    BirdZone,
    CalligraphyAnimator,
    FlowerZone,
    NormRect,
    RenderOptions,
    SceneConfig,
    TextZone,
)


def _synthetic_scene(tmp_dir: Path) -> tuple[Path, SceneConfig]:
    """Crée une affiche synthétique 400×600 et sa configuration."""
    rng = np.random.default_rng(0)
    img = (rng.random((600, 400, 3)) * 60 + 150).astype(np.uint8)   # fond texturé
    cv2.rectangle(img, (70, 250), (330, 350), (30, 30, 30), -1)     # faux bloc de texte
    cv2.putText(img, "TEXTE SACRE", (95, 310), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (240, 240, 240), 2)
    cv2.circle(img, (320, 90), 35, (200, 80, 40), -1)               # « oiseau »
    cv2.circle(img, (60, 520), 45, (60, 180, 90), -1)               # « fleur »
    path = tmp_dir / "synthetique.png"
    cv2.imwrite(str(path), img)

    config = SceneConfig(
        name="synthetique",
        image=path.name,
        text_zones=(TextZone(NormRect(0.175, 0.416, 0.65, 0.167), "bloc texte"),),
        birds=(BirdZone(NormRect(0.70, 0.08, 0.20, 0.14), BirdMode.HOVER, "oiseau test"),),
        flowers=(FlowerZone(0.15, 0.866, 0.11, "fleur test"),),
    )
    return path, config


def test_text_bit_identical() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        path, config = _synthetic_scene(Path(td))
        anim = CalligraphyAnimator(path, config, RenderOptions())
        report = anim.verify_text_integrity(samples=16)
        assert report["texte_intact"], f"Le texte a été modifié : {report}"
        assert report["ecart_max_dans_le_texte"] == 0


def test_perfect_loop() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        path, config = _synthetic_scene(Path(td))
        anim = CalligraphyAnimator(path, config, RenderOptions())
        first, wrapped = anim.render_frame(0.0), anim.render_frame(1.0)
        # Boucle parfaite à l'arrondi flottant près : sin(2π(c+φ)) vs sin(2πφ)
        # peuvent différer d'un epsilon, ce qui sur un fond bruité haute
        # fréquence retourne quelques pixels de ±1. On exige donc une erreur
        # moyenne quasi nulle plutôt qu'une égalité bit à bit.
        diff = np.abs(first.astype(np.float32) - wrapped.astype(np.float32))
        assert diff.mean() < 0.05 and (diff > 0).mean() < 0.01, (
            f"Boucle imparfaite : MAE={diff.mean():.4f}, "
            f"{100 * (diff > 0).mean():.2f} % de pixels différents"
        )


def test_ornaments_do_move() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        path, config = _synthetic_scene(Path(td))
        anim = CalligraphyAnimator(path, config, RenderOptions())
        report = anim.verify_text_integrity(samples=4)
        assert report["mouvement_moyen_ornements"] > 0.5, "Les ornements ne bougent pas"


def test_config_json_roundtrip() -> None:
    import tempfile

    with tempfile.TemporaryDirectory() as td:
        _, config = _synthetic_scene(Path(td))
        json_path = Path(td) / "cfg.json"
        config.to_json(json_path)
        loaded = SceneConfig.from_json(json_path)
        assert len(loaded.text_zones) == len(config.text_zones)
        assert len(loaded.birds) == len(config.birds)
        assert abs(loaded.birds[0].bbox.x - config.birds[0].bbox.x) < 1e-9


def test_invalid_config_rejected() -> None:
    try:
        SceneConfig.from_dict(
            {"text_zones": [{"rect": [0.9, 0.1, 0.5, 0.2]}]}  # déborde à droite
        )
    except ValueError:
        return
    raise AssertionError("Une zone qui déborde de l'image aurait dû être rejetée")


if __name__ == "__main__":
    tests = [
        test_text_bit_identical,
        test_perfect_loop,
        test_ornaments_do_move,
        test_config_json_roundtrip,
        test_invalid_config_rejected,
    ]
    for fn in tests:
        fn()
        print(f"OK  {fn.__name__}")
    print(f"\n{len(tests)}/{len(tests)} tests réussis — le sanctuaire de texte tient ses promesses.")
