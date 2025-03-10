"""
Fichier contenant la page "Détection d'anomalies" de l'application.
"""

import streamlit as st

from src.app.ui_components import show_navbar


def show():
    """
    Affiche la page "Détection d'anomalies".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/policy_alert: Détection d'anomalies")
