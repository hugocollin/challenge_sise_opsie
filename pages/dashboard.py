"""
Fichier contenant la page "Tableau de bord" de l'application.
"""

import streamlit as st
import plotly.express as px

from src.app.ui_components import show_navbar


@st.cache_data(show_spinner=False)
def get_counts(_data_filtre, column_name):
    """
    Calcule et met en cache les comptes de valeurs pour une colonne donnée.
    """
    counts = _data_filtre[column_name].value_counts().reset_index().compute()
    return counts

def show():
    """
    Affiche la page "Tableau de bord" avec des graphiques optimisés.
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/dashboard: Tableau de bord")

    # Récupération des données
    data = st.session_state.data

    # Filtrage par plage de ports (RFC 6056)
    with st.container(border=True):
        port_min, port_max = st.slider(
            "Filtrage par plage de ports (RFC 6056)",
            min_value=1, max_value=65535,
            value=(1, 65535)
        )
        data_filtre = data[(data['portdst'] >= port_min) & (data['portdst'] <= port_max)]

    cols = st.columns(2)

    with cols[0]:
        # Flux TCP et UDP en camembert
        with st.container(border=True):
            protocol_counts = get_counts(data_filtre, 'proto')
            protocol_counts.columns = ['proto', 'count']
            fig_protocol = px.pie(
                protocol_counts,
                names='proto',
                values='count',
                title="Répartition des flux",
                hole=0.5
            )
            fig_protocol.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_protocol, use_container_width=True)

    with cols[1]:
        # Connexions acceptées et refusées en camembert
        with st.container(border=True):
            action_counts = get_counts(data_filtre, 'action')
            action_counts.columns = ['action', 'count']
            fig_action = px.pie(
                action_counts,
                names='action',
                values='count',
                title="Répartition des connexions",
                hole=0.5
            )
            fig_action.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_action, use_container_width=True)

    # # Tableau interactif des données (renderDataTable) avec filtrage dynamique
    # st.subheader("Tableau interactif des logs")
    # ip_filter = st.text_input("Filtrer par IP")
    # protocol_filter = st.selectbox("Filtrer par protocole", options=["", "TCP", "UDP"])
    # action_filter = st.selectbox("Filtrer par action", options=["", "accept", "refuse"])

    # data_table = data_filtre.copy()
    # if ip_filter:
    #     data_table = data_table[data_table['ip'].str.contains(ip_filter)]
    # if protocol_filter:
    #     data_table = data_table[data_table['protocol'] == protocol_filter]
    # if action_filter:
    #     data_table = data_table[data_table['action'] == action_filter]

    # st.dataframe(data_table)

    # # Statistiques principales
    # st.subheader("Statistiques principales")

    # # Top 5 des IP les plus émettrices
    # top_ips = data_filtre['ip'].value_counts().head(5)
    # st.write("**Top 5 des IP émettrices :**")
    # st.table(top_ips.reset_index().rename(columns={'index': 'IP', 'ip': 'Nombre de connexions'}))

    # # Top 10 des ports inférieurs à 1024 les plus autorisés
    # ports_autorises = data_filtre[(data_filtre['port'] < 1024) & (data_filtre['action'] == 'accept')]
    # top_ports = ports_autorises['port'].value_counts().head(10)
    # st.write("**Top 10 des ports (<1024) les plus autorisés :**")
    # st.table(top_ports.reset_index().rename(columns={'index': 'Port', 'port': 'Nombre d\'acceptations'}))

    # # Adresses hors du plan d’adressage universitaire
    # # Ici on considère que le plan d'adressage universitaire commence par "192.168"
    # st.write("**Adresses hors du plan d’adressage universitaire :**")
    # hors_plan = data_filtre[~data_filtre['ip'].str.startswith("192.168")]
    # st.table(hors_plan[['ip']].drop_duplicates())
