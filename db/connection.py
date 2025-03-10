import mysql.connector

# Configuration de la connexion
config = {
    "host": "localhost",  # Nom du conteneur MariaDB
    "user": "root",
    "password": "mypass123",
    "database": "mysql",  # Remplace par le nom de ta base de données si nécessaire
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
