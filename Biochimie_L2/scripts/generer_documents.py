"""Régénère les figures puis les deux documents Word du chapitre de glucides.

Depuis le dossier Biochimie_L2 :
    python -m pip install -r requirements.txt
    python scripts/generer_documents.py
"""
from generate_illustrations import make_all
from generate_cours import build as build_cours
from generate_corrige import build as build_corrige


def main():
    make_all()
    cours = build_cours()
    corrige = build_corrige()
    print('\nDocuments générés :')
    print(cours)
    print(corrige)


if __name__ == '__main__':
    main()
