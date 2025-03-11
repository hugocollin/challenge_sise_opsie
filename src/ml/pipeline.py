import pandas as pd
import numpy as np
import polars as pl
import ipaddress
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from lightgbm import LGBMClassifier
from sklearn.metrics import classification_report

# Charger le fichier .parquet avec Polars
df = pl.read_parquet("C:/Users/akaramoko/Desktop/challenge_sise_opsie/src/ml/log_export.parquet")

# Afficher les colonnes pour vérification
#print("Colonnes disponibles :", df.columns)

# Suppression des colonnes inutiles si elles existent
cols_to_drop = ['Interface_out', 'interface_in', 'divers']
df = df.drop([col for col in cols_to_drop if col in df.columns])

# Conversion Polars → Pandas pour utiliser Scikit-learn
df = df.to_pandas()

# Supprimer les valeurs manquantes
df = df.dropna()

# Conversion des adresses IP en entiers
def ip_to_int(ip):
    try:
        return int(ipaddress.ip_address(ip))
    except ValueError:
        return 0

df['ipsrc'] = df['ipsrc'].apply(ip_to_int)
df['ipdst'] = df['ipdst'].apply(ip_to_int)

# Définir la variable cible : si l'action est DENY, on met 1 (suspect)
df['action'] = df['action'].apply(lambda x: 1 if x == 'DENY' else 0)

# Encodage des variables catégorielles avec One-Hot Encoding
df = pd.get_dummies(df, columns=['proto'], drop_first=True)

# Conversion de la colonne 'date'
df['date'] = pd.to_datetime(df['date'])

# Vérification des valeurs manquantes
missing_values = df.isnull().sum()
#print("Valeurs manquantes par colonne :\n", missing_values)

# Sélection des features (X) et de la cible (y)
X = df.drop(columns=['action', 'date'])  # On enlève 'date' car ce n'est pas une feature utile ici
y = df['action']

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
ip_activity = df[df['action'] == 1]['ipsrc'].value_counts().head(20)
plt.figure(figsize=(10,6))
sns.barplot(x=ip_activity.values, y=ip_activity.index, palette='Reds')
plt.xlabel('Nombre d\'activités suspectes')
plt.title('Top 20 des adresses IP suspectes les plus actives')
plt.show()