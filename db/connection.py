import mysql.connector
import os
from dotenv import load_dotenv



# Charger les variables d'environnement du fichier .env
load_dotenv()

# Configuration de la connexion à MariaDB
config = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "port": int(os.getenv("DB_PORT")),
}


try:
    # Connexion à MariaDB
    conn = mysql.connector.connect(**config)  
    if conn.is_connected():
        print("Connexion réussie à MariaDB")  
    # Fermer la connexion
    conn.close()

except mysql.connector.Error as err:
    print(f"Erreur: {err}")
