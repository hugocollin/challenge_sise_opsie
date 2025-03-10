# README : Challenge SISE x OPSIE

## Table des matières
- [Description](#description)
- [Fonctionnalités principales](#fonctionnalités-principales)
- [Structure du projet](#structure-du-projet)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Contribution](#contribution)
- [Auteurs](#auteurs)

## Description

Le projet SISE x OPSIE est un challenge académique visant à analyser et visualiser les logs d’un firewall Iptables dans un environnement cloud et on-premise. L’objectif est de fournir un tableau de bord interactif permettant d’explorer les flux réseaux, d’identifier des tendances et d’évaluer la sécurité du système d’information. Ce projet intègre également une composante Machine Learning pour la détection d’anomalies et d’intrusions à partir des journaux de connexion.

### Fonctionnalités principales

- Analyse descriptive :

- Visualisation interactive : 

- Détection d'anomalies : 

### Structure du projet

```bash
├── .streamlit
│   └── config.toml
├── docs
│   └── README.md
├── pages
│   ├── analyze.py
│   ├── detection.py
│   ├── home.py
│   └── visualisation.py
├── src
│   ├── app
│   │   └── ui_components.py
│   ├── db
│   │   └── connection.py
│   └── ml
│       └── ...
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── docker-requirements.txt
├── dockerfile
├── main.py
└── requirements.txt
```

## Installation

Pour installer ce projet, clonez le dépôt sur votre machine locale, en utilisant la commande suivante :

```bash
git clone https://github.com/hugocollin/challenge_sise_opsie
```

## Utilisation

Pour utiliser cette application vous avez 3 méthodes :

### I. Utilisez l'application en local

1. Installez et activez un environnement Python avec une version 3.12.

2. Ouvrez votre terminal et déplacez-vous à la racine du projet.

3. Exécutez la commande suivante pour installer les dépendances du projet :

```bash
pip install -r docker-requirements.txt
```

4. Exécutez la commande suivante pour lancer l'application :

```bash
streamlit run main.py
```

5. Ouvrez votre navigateur et accédez à l'adresse suivante : [http://localhost:8501](http://localhost:8501)

### II. Utilisez l'application avec Docker

1. Installez et demarrez [Docker Desktop](https://www.docker.com/products/docker-desktop/) sur votre machine.

2. Ouvrez votre terminal et déplacez-vous à la racine du projet.

3. Exécutez la commande suivante pour construire l'image Docker :

```bash
docker-compose up --build
```

4. Ouvrez votre navigateur et accédez à l'adresse suivante : [http://localhost:8501](http://localhost:8501)

### III. Utilisez l'application en ligne

Ouvrez votre navigateur et accédez à l'adresse suivante : [https://challenge-sise-opsie.streamlit.app](https://challenge-sise-opsie.streamlit.app)

## Contribution

Toutes les contributions sont les bienvenues ! Voici comment vous pouvez contribuer :

1. Forkez le projet.
2. Créez votre branche de fonctionnalité  (`git checkout -b feature/AmazingFeature`).
3. Commitez vos changements (`git commit -m 'Add some AmazingFeature'`).
4. Pushez sur la branche (`git push origin feature/AmazingFeature`).
5. Ouvrez une Pull Request. 

## Auteurs

Cette application a été développée par [KPAMEGAN Falonne](https://github.com/marinaKpamegan), [KARAMOKO Awa](https://github.com/karamoko17), [POGNANTE Jules](https://github.com/KirkVanHouten), [BELIN Thomas](https://gitlab.com/Thomasp1914935) et [COLLIN Hugo](https://github.com/hugocollin), dans le cadre du Master 2 SISE et OPSIE.