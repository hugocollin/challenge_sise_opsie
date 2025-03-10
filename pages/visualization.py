"""
Fichier contenant la page "Visualisation interactive" de l'application.
"""

import streamlit as st

from src.app.ui_components import show_navbar


def show():
    """
    Affiche la page "Visualisation interactive".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title("Visualisation interactive")
