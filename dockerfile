# Utilisation d'une image Python
FROM python:3.12

# Installation des dépendances système
RUN apt-get update && apt-get install -y locales && \
    sed -i '/fr_FR.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen

# Définition des variables d'environnement pour le français
ENV LANG=fr_FR.UTF-8 \
    LANGUAGE=fr_FR:fr \
    LC_ALL=fr_FR.UTF-8

# Copie des fichiers de configuration des dépendances
COPY docker-requirements.txt .

# Installation des dépendances Python
RUN pip install --upgrade pip
RUN pip install -r docker-requirements.txt

# Définition du répertoire de travail dans le conteneur
WORKDIR /app

# Copie des fichiers de l'application
COPY . .

# Ouverture du port Streamlit
EXPOSE 8501

# Démarrage de l'application Streamlit
CMD ["streamlit", "run", "main.py"]