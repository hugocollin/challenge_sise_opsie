import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from src.app.ui_components import show_navbar
import ipaddress
import plotly.express as px
import dask.dataframe as dd
import seaborn as sns
import matplotlib.pyplot as plt

def ip2int(ip):
    return int(ipaddress.ip_address(ip))

def show():
    """
    Affiche la page "Détection d'anomalies".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/policy_alert: Détection d'anomalies")

    # Récupération des données
    data = st.session_state["data"].dropna()

    # Conversion en DataFrame Dask si nécessaire
    if not isinstance(data, dd.DataFrame):
        data = dd.from_pandas(data, npartitions=4)

    tab1, tab2, tab3, tab4 = st.tabs(["Apprentissage supervisé", "Clustering", "Analyse des connexions", "Détection des anomalies"])

    with tab1:
        st.subheader("🔍 Apprentissage supervisé")
        st.write("Section en cours de développement.")

    with tab2:
        st.subheader("📊 Analyse des connexions et clustering")

        # Calcul des statistiques
        nb_total = data.groupby('ipsrc').size().reset_index().rename(columns={0: 'nb_total'})
        nb_deny = data[data['action'] == 'DENY'].groupby('ipsrc').size().reset_index().rename(columns={0: 'nb_deny'})
        nb_admit = data[data['action'] == 'PERMIT'].groupby('ipsrc').size().reset_index().rename(columns={0: 'nb_admit'})
        ports_autorises = data[data['action'] == 'PERMIT'].groupby('ipsrc')['portdst'].nunique().reset_index()
        ports_autorises = ports_autorises.rename(columns={'portdst': 'nb_ports_autorises'})

        # Fusion des statistiques
        df_stats = nb_total.merge(nb_deny, on='ipsrc', how='left') \
                          .merge(nb_admit, on='ipsrc', how='left') \
                          .merge(ports_autorises, on='ipsrc', how='left')

        df_stats = df_stats.fillna({'nb_deny': 0, 'nb_admit': 0, 'nb_ports_autorises': 0})
        df_stats = df_stats.astype({'nb_total': int, 'nb_deny': int, 'nb_admit': int, 'nb_ports_autorises': int})
        df_stats = df_stats.compute()

        # Convertir les IPs en entiers
        df_stats['ipsrc_int'] = df_stats['ipsrc'].apply(ip2int)

        # Affichage du DataFrame
        st.dataframe(df_stats, use_container_width=True)

        # Clustering avec K-Means
        selected_cols = ['nb_total', 'nb_deny', 'nb_admit', 'nb_ports_autorises', 'ipsrc_int']
        df_cluster = df_stats[selected_cols]
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_cluster)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df_stats['Cluster'] = kmeans.fit_predict(df_scaled)

        # Visualisation interactive avec Plotly
        fig = px.scatter(df_stats, x='nb_total', y='nb_ports_autorises',
                         color=df_stats['Cluster'].astype(str),
                         hover_data=['ipsrc'],
                         title='Clusters des IPs sources',
                         labels={'Cluster': 'Groupe', 'nb_total': 'Nombre total de connexions', 'nb_ports_autorises': 'Nombre de ports autorisés'},
                         color_discrete_sequence=px.colors.qualitative.Set1)

        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("📈 Analyse des connexions")
        # Histogramme des connexions par IP
        fig_hist = px.bar(df_stats, x='ipsrc', y='nb_total', title="Nombre de connexions par IP",
                          labels={'ipsrc': 'Adresse IP', 'nb_total': 'Nombre de connexions'},
                          text_auto=True)
        st.plotly_chart(fig_hist, use_container_width=True)

        # Matrice de corrélation
        # fig_corr, ax = plt.subplots()
        # sns.heatmap(df_cluster.corr(), annot=True, cmap="coolwarm", ax=ax)
        # st.pyplot(fig_corr)

    with tab4:
        st.subheader("🚨 Détection des anomalies avec Isolation Forest")
        iso_forest = IsolationForest(contamination=0.05, random_state=42)
        df_stats['Anomalie'] = iso_forest.fit_predict(df_scaled)
        df_stats['Anomalie'] = df_stats['Anomalie'].map({1: 'Normal', -1: 'Anomalie'})

        # Visualisation des anomalies
        fig_anomalies = px.scatter(df_stats, x='nb_total', y='nb_ports_autorises', color='Anomalie',
                                   title='Détection des anomalies', hover_data=['ipsrc'])
        st.plotly_chart(fig_anomalies, use_container_width=True)
