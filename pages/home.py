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
    st.title("Accueil")
