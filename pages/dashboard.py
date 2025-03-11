"""
Fichier contenant la page "Tableau de bord" de l'application.
"""

import streamlit as st
import polars as pl
import plotly.express as px

from src.app.ui_components import show_navbar

@st.cache_data(show_spinner=False)
def compute_counts(port_min: int, port_max: int, column_name: str, 
                   action_filter: bool = False):
    """
    Calcul et mise en cache des comptes pour une colonne donnée 
    en tenant compte d'un éventuel filtre sur l'action.
    """
    data = st.session_state.data
    data_filtre = data.filter((pl.col("portdst") >= port_min) & (pl.col("portdst") <= port_max))
    if action_filter:
        data_filtre = data_filtre.filter(pl.col("action") == "PERMIT")
    counts = data_filtre.group_by(column_name).agg(pl.count().alias("count"))
    
    return counts.to_pandas()

def show():
    """
    Affiche la page "Tableau de bord" avec des graphiques optimisés.
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/dashboard: Tableau de bord")

    # Filtrage par plage de ports (RFC 6056)
    with st.container(border=True):
        port_min, port_max = st.slider(
            "Filtrage par plage de ports (RFC 6056)",
            min_value=1, max_value=65535,
            value=(1, 65535)
        )

    cols = st.columns(2)

    with cols[0]:
        # Top 5 des IP émettrices
        with st.container(border=True):
            top_ips = compute_counts(port_min, port_max, 'ipsrc')
            top_ips.columns = ['ipsrc', 'count']
            top_ips = top_ips.sort_values(by='count', ascending=False).head(5).reset_index(drop=True)
            st.write("**Top 5 des IP émettrices :**")
            for i, row in top_ips.iterrows():
                st.write(f"**{i+1}.** `{row['ipsrc']}` : {row['count']} connexions")

        # Adresses hors du plan d’adressage universitaire
        with st.container(border=True):
            st.write("**Adresses hors du plan d’adressage universitaire :**")
            # Exemple de code pour afficher ces adresses (à ajuster si besoin)
            # non_uni = compute_counts(port_min, port_max, 'ipsrc')
            # non_uni.columns = ['ipsrc', 'count']
            # non_uni = non_uni[~non_uni['ipsrc'].str.startswith("192.168")].sort_values(by='count', ascending=False)
            # for i, row in non_uni.iterrows():
            #     st.write(f"**-** `{row['ipsrc']}` : {row['count']} connexions")

        # Répartition des connexions
        with st.container(border=True):
            action_counts = compute_counts(port_min, port_max, 'action')
            action_counts.columns = ['action', 'count']
            fig_action = px.pie(
                action_counts,
                names='action',
                values='count',
                title="Répartition des connexions",
                hole=0.5,
                color='action',
                color_discrete_map={'PERMIT': 'green', 'DENY': 'red'}
            )
            fig_action.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_action, use_container_width=True)

        # Répartition des règles
        with st.container(border=True):
            rule_counts = compute_counts(port_min, port_max, 'regle')
            rule_counts.columns = ['regle', 'count']
            fig_rule = px.pie(
                rule_counts,
                names='regle',
                values='count',
                title="Répartition des règles",
                hole=0.5
            )
            fig_rule.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_rule, use_container_width=True)

    with cols[1]:
        # Top 10 des ports inférieurs à 1024 les plus autorisés
        with st.container(border=True):
            st.write("**Top 10 des ports (< 1024) les plus autorisés :**")
            top_ports = compute_counts(port_min, port_max, 'portdst', action_filter=True)
            top_ports.columns = ['portdst', 'count']
            top_ports = top_ports.sort_values(by='count', ascending=False).head(10).reset_index(drop=True)
            for i, row in top_ports.iterrows():
                st.write(f"**{i+1}.** Port `{row['portdst']}` : {row['count']} connexions")

        # Répartition des protocoles
        with st.container(border=True):
            protocol_counts = compute_counts(port_min, port_max, 'proto')
            protocol_counts.columns = ['proto', 'count']
            fig_protocol = px.pie(
                protocol_counts,
                names='proto',
                values='count',
                title="Répartition des protocoles",
                hole=0.5
            )
            fig_protocol.update_traces(textinfo='percent+value')
            st.plotly_chart(fig_protocol, use_container_width=True)
