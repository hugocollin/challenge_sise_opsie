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

    # Description de l'application
    st.write("Le projet SISE x OPSIE est un challenge académique visant à analyser et visualiser les logs d’un firewall Iptables dans un environnement cloud et on-premise. L’objectif est de fournir un tableau de bord interactif permettant d’explorer les flux réseaux, d’identifier des tendances et d’évaluer la sécurité du système d’information. Ce projet intègre également une composante Machine Learning pour la détection d’anomalies et d’intrusions à partir des journaux de connexion.")

    # Fonctionnalités de l'application
    cols = st.columns(3)

    with cols[0]:
        with st.container(border=True):
            st.write("**:material/table: Données**")
            st.write("*Texte descriptif disponible ultérieurement*")

    with cols[1]:
        with st.container(border=True):
            st.write("**:material/dashboard: Tableau de bord**")
            st.write("*Texte descriptif disponible ultérieurement*")

    with cols[2]:
        with st.container(border=True):
            st.write("**:material/policy_alert: Détection d'anomalies**")
            st.write("*Texte descriptif disponible ultérieurement*")

    # Crédits de l'application
    st.write(
        "*L'application est Open Source et disponible sur "
        "[GitHub](https://github.com/hugocollin/challenge_sise_opsie). "
        "Celle-ci a été développée par "
        "[KPAMEGAN Falonne](https://github.com/marinaKpamegan), "
        "[KARAMOKO Awa](https://github.com/karamoko17), "
        "[POGNANTE Jules](https://github.com/KirkVanHouten), "
        "[BELIN Thomas](https://gitlab.com/Thomasp1914935) "
        "et [COLLIN Hugo](https://github.com/hugocollin), dans le cadre du Master 2 SISE et OPSIE.*"
    )
