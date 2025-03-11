import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import ipaddress
import plotly.express as px
import polars as pl
import pandas as pd

from src.app.ui_components import show_navbar

import numpy as np
import polars as pl
import ipaddress
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report

def ip2int(ip):
    """
    Convertit une adresse IP en entier.
    """
    return int(ipaddress.ip_address(ip))


@st.cache_data(show_spinner=False)
def load_data():
    """
    Charge les données et calcule les statistiques.
    """

    # Récupération des données
    data = st.session_state["data"].drop_nulls()
    data = pl.DataFrame(data)

    # Calcul des statistiques
    nb_total = data.group_by("ipsrc").len().rename({"len": "nb_total"})
    nb_deny = data.filter(pl.col("action") == "DENY").group_by("ipsrc").len().rename({"len": "nb_deny"})
    nb_admit = data.filter(pl.col("action") == "PERMIT").group_by("ipsrc").len().rename({"len": "nb_admit"})
    ports_autorises = (
        data.filter(pl.col("action") == "PERMIT")
        .group_by("ipsrc")
        .agg(pl.col("portdst").n_unique().alias("nb_ports_autorises"))
    )

    # Fusion des statistiques
    df_stats = (
        nb_total.join(nb_deny, on="ipsrc", how="left")
        .join(nb_admit, on="ipsrc", how="left")
        .join(ports_autorises, on="ipsrc", how="left")
        .fill_null(0)
    )

    # Convertir les colonnes en int
    df_stats = df_stats.with_columns(
        [pl.col(c).cast(pl.Int32) for c in ["nb_total", "nb_deny", "nb_admit", "nb_ports_autorises"]]
    )

    # Convertir les IPs en entiers
    df_stats = df_stats.with_columns(
        pl.col("ipsrc").map_elements(ip2int, return_dtype=pl.Int64).alias("ipsrc_int")
    )

    return df_stats


def show():
    """
    Affiche la page "Détection d'anomalies".
    """
    # Barre de navigation
    show_navbar()

    # Titre de la page
    st.title(":material/policy_alert: Détection d'anomalies")

    # Chargement des données
    df_stats = load_data()

    # Récupération des données
    data = st.session_state["data"].drop_nulls()
    data = pl.DataFrame(data)

    tab1, tab2, tab3 = st.tabs(["Apprentissage supervisé", "Clustering", "Analyse des connexions"])

    with tab1:
        st.subheader("Classification des adresses IP en fonction de leur comportement")

        # Conversion Polars → Pandas pour utiliser Scikit-learn
        data1 = data.to_pandas()

        # Supprimer les valeurs manquantes
        data1 = data1.dropna()


        # Conversion des adresses IP en entiers
        def ip_to_int(ip):
            try:
                return int(ipaddress.ip_address(ip))
            except ValueError:
                return 0

        data1['ipsrc'] = data1['ipsrc'].apply(ip_to_int)
        data1['ipdst'] = data1['ipdst'].apply(ip_to_int)

        # Définir la variable cible : si l'action est DENY, on met 1 (suspect)
        data1['action'] = data1['action'].apply(lambda x: 1 if x == 'DENY' else 0)

        # Encodage des variables catégorielles avec One-Hot Encoding
        data1['proto'] = data1['proto'].astype('category').cat.codes

        # Conversion de la colonne 'date'
        data1['date'] = pd.to_datetime(data1['date'])

        # Vérification des valeurs manquantes
        missing_values = data1.isnull().sum()
        #print("Valeurs manquantes par colonne :\n", missing_values)

        # Sélection des features (X) et de la cible (y)
        X = data1.drop(columns=['action', 'date'])  # On enlève 'date' car ce n'est pas une feature utile ici
        y = data1['action']

        # Séparation en train et test
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Utiliser LightGBM au lieu de RandomForest
        model = LGBMClassifier(n_estimators=100, learning_rate=0.1)
        model.fit(X_train, y_train)

        # 8️⃣ Évaluer le modèle
        y_pred = model.predict(X_test)
        #print("Classification Report:")
        #print(classification_report(y_test, y_pred))

        # Visualisation des IP suspectes les plus actives
        ip_activity = data1[data1['action'] == 1]['ipsrc'].value_counts().head(20)
        plt.figure(figsize=(10,6))
        sns.barplot(x=ip_activity.values, y=ip_activity.index, palette='Reds')
        plt.xlabel('Nombre d\'activités suspectes')
        plt.title('Top 20 des adresses IP suspectes les plus actives')
        plt.show()

    with tab2:
        st.subheader("Analyse des connexions et clustering")

        # Affichage du DataFrame sans reconversion inutile
        st.dataframe(df_stats, use_container_width=True)

        # Clustering avec K-Means
        selected_cols = ["nb_total", "nb_deny", "nb_admit", "nb_ports_autorises", "ipsrc_int"]
        df_cluster = df_stats.select(selected_cols)
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_cluster.to_numpy())

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        df_stats = df_stats.with_columns(pl.Series(name="Cluster", values=kmeans.fit_predict(df_scaled)))

        # Visualisation interactive avec Plotly
        fig = px.scatter(
            df_stats.to_pandas(),
            x="nb_total",
            y="nb_ports_autorises",
            color=df_stats["Cluster"].to_pandas().astype(str),
            hover_data=["ipsrc"],
            title="Clusters des IPs sources",
            labels={
                "Cluster": "Groupe",
                "nb_total": "Nombre total de connexions",
                "nb_ports_autorises": "Nombre de ports autorisés",
            },
            color_discrete_sequence=px.colors.qualitative.Set1,
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Analyse des connexions")

        # Sélection des 20 IPs avec le plus de connexions
        df_top20 = df_stats.sort("nb_total", descending=True).head(20)

        # Création du graphe avec Plotly
        fig_hist = px.bar(
            df_top20.to_pandas(),
            x="ipsrc",
            y="nb_total",
            title="Top 20 des IPs avec le plus de connexions",
            labels={"ipsrc": "Adresse IP", "nb_total": "Nombre de connexions"},
            text_auto=True,
        )
        st.plotly_chart(fig_hist, use_container_width=True)
