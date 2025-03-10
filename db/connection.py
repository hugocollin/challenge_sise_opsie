import mysql.connector

# Configuration de la connexion
config = {
    "host": "localhost",  
    "user": "root",
    "password": "mypass123",
    "database": "mysql",  
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
