# README pour le Dashboard des Cinémas en France

## User Guide

### Prérequis

Assurez-vous que les éléments suivants sont installés :

- Python 3.9 ou une version ultérieure
- pip (gestionnaire de packages Python)

### Installation

1. Clonez le dépôt :

   ```bash
   git clone https://github.com/LazareGarcin/DataProject.git
   cd DataProject
   ```

2. Créez un environnement virtuel et activez-le :

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Sur Windows : `.venv\Scripts\activate`
   ```

3. Installez les dépendances nécessaires :

   ```bash
   pip install -r requirements.txt
   ```

4. Lancez le dashboard :

   ```bash
   python main.py
   ```

### Utilisation

- Ouvrez votre navigateur web et accédez à `http://127.0.0.1:8050` pour utiliser le dashboard.
- Explorez les visualisations des cinémas en France.

---

## Data

### Source

Les données utilisées dans ce projet sont issues de [OpenStreetMap](https://www.openstreetmap.org/) et compilées par [Opendatasoft](https://www.opendatasoft.com/).

### Structure

- Les données brutes sont stockées dans `data/raw/`.
- Les données nettoyées sont stockées dans `data/cleaned/` après traitement.
- Pour les données dynamiques, le script `get_data.py` gère leur récupération.

### Description

Le dataset inclut les informations suivantes :

- **Nom du cinéma :** Identifié par le champ `name`.
- **Enseigne :** Identifié sur le champ `marque`.
- **Identifiant CNC :** Disponible via le champ `ref_cnc`.
- **Capacité :** Nombre total de places.
- **Nombre d'écrans :** Décrit par le champ `screens`.
- **Heures d'ouverture :** Spécifiées par le champ `opening_hours`.
- **Géolocalisation :** Coordonnées fournies pour chaque cinéma.

---

## Guide Développeur

### Structure du Projet

```
data_project
|-- README.md
|-- assets
|   |-- image_cgr.png
|   |-- image_pathe.png
|   |-- image_ugc.png
|-- config.py
|-- data
|   |-- cleaned
|   │   |-- cleaneddata.csv
|   |-- raw
|       |-- dataset.csv
|-- main.py
|-- requirements.txt
|-- src
    |-- callbacks
    |   |-- __init__.py
    |   |-- circle_callback.py
    |   |-- content_callback.py
    |   |-- heatmap_callback.py
    |   |-- histogram_callback.py
    |   |-- map_callback.py
    |   |-- menu_callback.py
    |-- components
    |   |-- __init__.py
    |   |-- menu.py
    |-- pages
    |   |-- __init__.py
    |   |-- circle.py
    |   |-- heatmap.py
    |   |-- histogram.py
    |   |-- home.py
    |   |-- map.py
    |-- utils
        |-- clean_data.py
        |-- get_data.py
|-- video_dashboard_2.mp4
```

### Ajouter une Nouvelle Page

1. Créez un nouveau fichier dans `src/pages/`, par exemple `nouvelle_page.py`.
2. Créez un nouveau fichier dans src/callbacks/, par exemple `nouveau_callback.py`.
3. Implémentez le layout et les callbacks spécifiques à la page.
4. Ajoutez la nouvelle page à la navigation dans `menu.py`.
5. Importez et appelez le callback dans `main.py`.

### Scripts Clés

- **`main.py`** : Point d'entrée du dashboard.
- **`get_data.py`** : Récupère les données depuis OpenStreetMap et les stocke dans `data/raw/`.
- **`clean_data.py`** : Prépare et nettoie les données pour l'analyse.
- **`callbacks/`** : Contient les scripts pour gérer les interactions dynamiques (histogrammes, cartes, etc.).
- **`components/`** : Contient les composants réutilisables de l'interface utilisateur (ex. menu).
- **`pages/`** : Organise les différentes pages du dashboard.

---

## Rapport d'Analyse

### Principales Conclusions

1. La distribution géographique des cinémas montre une concentration notable dans les grandes villes.
2. La capacité moyenne des cinémas varie considérablement en fonction des régions.

---

## Droits d'Auteur

Nous déclarons sur l'honneur que le code fourni a été produit par notre groupe : Yacine Housny et Jordan Belcollin

Toutes les autres lignes sont notre travail original.&#x20;

---

## Vidéo

La vidéo de démonstration est disponible dans le dépôt sous le nom `video_dashboard_2.mp4`. Elle inclut :

- Le démarrage du projet.
- Les fonctionnalités principales.

---

