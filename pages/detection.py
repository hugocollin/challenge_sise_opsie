import streamlit as st
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import ipaddress
import plotly.express as px
import polars as pl


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
    df_stats = df_stats.with_columns(pl.col("ipsrc").map_elements(ip2int).alias("ipsrc_int"))

    return df_stats


def show():
    """
    Affiche la page "Détection d'anomalies".
    """
    # Titre de la page
    st.title(":material/policy_alert: Détection d'anomalies")

    # Chargement des données
    df_stats = load_data()

    tab1, tab2, tab3 = st.tabs(["Apprentissage supervisé", "Clustering", "Analyse des connexions"])

    with tab1:
        st.subheader("Apprentissage supervisé")
        st.write("Section en cours de développement.")

    with tab2:
        st.subheader("Analyse des connexions et clustering")

        # Calcul des statistiques
        # nb_total = data.group_by("ipsrc").len().rename({"len": "nb_total"})
        # nb_deny = data.filter(data["action"] == "DENY").group_by("ipsrc").len().rename({"len": "nb_deny"})
        # nb_admit = data.filter(data["action"] == "PERMIT").group_by("ipsrc").len().rename({"len": "nb_admit"})
        # ports_autorises = (
        #     data.filter(data["action"] == "PERMIT")
        #     .group_by("ipsrc")
        #     .agg(pl.col("portdst").n_unique().alias("nb_ports_autorises"))
        # )

        # # Fusion des statistiques
        # df_stats = (
        #     nb_total.join(nb_deny, on="ipsrc", how="left")
        #     .join(nb_admit, on="ipsrc", how="left")
        #     .join(ports_autorises, on="ipsrc", how="left")
        #     .fill_null(0)
        # )

        # Convertir les colonnes en int
        df_stats = df_stats.with_columns(
            [pl.col(c).cast(pl.Int32) for c in ["nb_total", "nb_deny", "nb_admit", "nb_ports_autorises"]]
        )

        # Convertir les IPs en entiers
        df_stats = df_stats.with_columns(pl.col("ipsrc").map_elements(ip2int).alias("ipsrc_int"))


        # Affichage du DataFrame
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


