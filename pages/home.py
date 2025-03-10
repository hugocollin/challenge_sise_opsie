"""
Fichier contenant la page "Accueil" de l'application.
"""

import streamlit as st

from src.app.ui_components import show_navbar


def show():
    """
    Affiche la page "Accueil".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title("Challenge SISE x OPSIE")

    # Crédits de l'application
    st.write(
        "*L'application est Open Source et disponible sur "
        "[GitHub](https://github.com/hugocollin/challenge_sise_opsie). "
        "Celle-ci a été développée par "
        "[KPAMEGAN Falonne](https://github.com/marinaKpamegan), "
        "[KARAMOKO Awa](https://github.com/karamoko17), "
        "[POGNANTE Jules](https://github.com/KirkVanHouten), "
        "[BELIN Thomas](https://github.com/Thomasp1914935) "
        "et [COLLIN Hugo](https://github.com/hugocollin), dans le cadre du Master 2 SISE et OPSIE.*"
    )