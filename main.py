"""
Fichier principal de l'application.
"""

import os
import streamlit as st

from dotenv import load_dotenv, find_dotenv
from src.db.connection import load_parquet

# Configuration de la page
st.set_page_config(page_title="Challenge SISE x OPSIE", page_icon=":material/policy:", layout="wide")

# Récupération de l'environnement d'exécution
load_dotenv(find_dotenv())
PLATFORM = os.getenv("PLATFORM")

# Récupération de la page à afficher
page = st.query_params.page if "page" in st.query_params else "home"

# Table de correspondance pour la navigation
page_mapping = {
    "home": "pages.home",
    "data": "pages.data",
    "dashboard": "pages.dashboard",
    "detection": "pages.detection"
}

# Mise à jour de l'URL
st.query_params.page = page

# Import du module de la page à afficher
module_name = page_mapping.get(page, "pages.home")
page_module = __import__(module_name, fromlist=["show"])

# Chargement des données
if "data" not in st.session_state:
    data = load_parquet()
    st.session_state["data"] = data

# Affichage de la page
page_module.show()
