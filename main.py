"""
Fichier principal de l'application.
"""

import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Pokemon TCGP Companion", page_icon=":material/polymer:")

# Récupération de la page à afficher
page = st.query_params.page if "page" in st.query_params else "home"

# Table de correspondance pour la navigation
page_mapping = {
    "home": "pages.home",
    "analyze": "pages.analyze",
    "visualization": "pages.visualization",
    "detection": "pages.detection"
}

# Mise à jour de l'URL
st.query_params.page = page

# Import du module de la page à afficher
module_name = page_mapping.get(page, "pages.home")
page_module = __import__(module_name, fromlist=["show"])

# Affichage de la page
page_module.show()