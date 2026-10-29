# Biochimie structurale L2 — La structure des glucides

Support pédagogique original correspondant au **TD n°1 fourni** : stéréochimie des oses, projections de Fischer et Haworth, anomères, liaisons osidiques et pouvoir réducteur.

## Livrables Word

| Fichier | Contenu |
|---|---|
| `documents/Cours_Biochimie_L2_Structure_des_glucides.docx` | Cours de 23 pages : objectifs, notions, méthodes, 16 figures pédagogiques, tableaux, autoévaluation et fiche de révision. |
| `documents/Corrige_detaille_TD1_Biochimie_L2.docx` | Corrigé de 19 pages : les quatre exercices, réponses justifiées, calculs, structures de Haworth et signalement des ambiguïtés de l’énoncé. |

Les fichiers sont modifiables dans Word. Les figures sont intégrées ; les en-têtes, pieds de page, numéros de page, tableaux et styles sont inclus. Les documents finaux ne contiennent aucun filigrane.

## Régénération avec Python

Depuis ce dossier :

```bash
python -m pip install -r requirements.txt
python scripts/generer_documents.py
python scripts/verifier_documents.py
```

- `scripts/generate_illustrations.py` : figures scientifiques originales avec matplotlib.
- `scripts/docx_helpers.py` : styles et composants de mise en page python-docx.
- `scripts/generate_cours.py` : contenu et structure du cours.
- `scripts/generate_corrige.py` : contenu et structure du corrigé.
- `scripts/verifier_documents.py` : contrôles structurels des fichiers produits.

## Conventions et points de rigueur

- Série D/L déterminée par le dernier carbone chiral, indépendamment du signe optique.
- Carbone anomérique : C1 pour le glucose, C2 pour le fructose.
- Orientation de Haworth standard précisée ; rotation de 180° du cycle fructose dans le saccharose explicitée.
- Exercice 3 : « l’isomère » est interprété comme l’énantiomère L-glucose, avec signalement des autres possibilités.
- Exercice 3 : le diholoside est construit comme le saccharose en reliant les deux carbones anomériques ; cette hypothèse est annoncée.
- Exercice 4 : les noms β-lactose et α-maltose respectent la configuration imposée à l’extrémité réductrice.

Le PDF source est conservé dans `sources/TD1_source.pdf`. Ce support n’est pas un corrigé officiel de l’enseignant.
