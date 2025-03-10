"""
Fichier contenant les composants de l'interface utilisateur.
"""

import streamlit as st

def navigate_to(page):
    """
    Redirige l'utilisateur vers une page spécifique.

    Args:
        page (str): Nom de la page.
    """
    st.query_params.page = page
    st.rerun()

def show_navbar():
    """
    Affiche la barre de navigation.
    """
    with st.sidebar:
        # Nom de l'application
        st.title("Challenge SISE x OPSIE")

        # Bouton "Accueil"
        if st.button(label="Accueil", icon=":material/home:", use_container_width=True):
            navigate_to("home")

        # Bouton "Analyse descriptive"
        if st.button(label="Analyse descriptive", icon=":material/search_insights:", use_container_width=True):
            navigate_to("analyze")

        # Bouton "Visualisation interactive"
        if st.button(label="Visualisation interactive", icon=":material/dashboard:", use_container_width=True):
            navigate_to("visualization")

        # Bouton "Détection d'anomalies"
        if st.button(label="Détection d'anomalies", icon=":material/policy_alert:", use_container_width=True):
            navigate_to("detection")
