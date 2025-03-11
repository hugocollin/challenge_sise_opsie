"""
Fichier contenant la page "Données" de l'application.
"""

import math
import streamlit as st

from src.app.ui_components import show_navbar


def show():
    """
    Affiche la page "Données".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/table: Données")

    # Récupération des données
    data = st.session_state["data"]

    # Paramètres de pagination
    if "total_rows" not in st.session_state:
        st.session_state["total_rows"] = data.height
    total_rows = st.session_state["total_rows"]

    if "page" not in st.session_state:
        st.session_state["page"] = 1
    page_size = 100
    total_pages = math.ceil(total_rows / page_size)

    start_idx = (st.session_state.page - 1) * page_size

    # Chargement uniquement des données de la page actuelle
    df_page = data.slice(start_idx, page_size).to_pandas()
    st.dataframe(df_page)

    cols = st.columns([3, 7, 10])

    # Sélecteur de page
    with cols[0]:
        st.number_input(
            "Sélectionnez la page",
            min_value=1,
            max_value=total_pages,
            step=1,
            key="page"
        )

    # Informations sur la pagination
    with cols[1]:
        st.write(f"Affichage des lignes {start_idx} à {min(start_idx+page_size, total_rows)} sur {total_rows}")

    # data_table = data_filtre.copy()
    # if ip_filter:
    #     data_table = data_table[data_table['ip'].str.contains(ip_filter)]
    # if protocol_filter:
    #     data_table = data_table[data_table['protocol'] == protocol_filter]
    # if action_filter:
    #     data_table = data_table[data_table['action'] == action_filter]
