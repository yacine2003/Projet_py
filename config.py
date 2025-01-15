DATA_URL = "https://public.opendatasoft.com/explore/dataset/osm-france-cinema/download/?format=csv"

# Chemins des fichiers
RAW_DATA_PATH = "data/raw/dataset.csv"
CLEANED_DATA_PATH = "data/cleaned/cleaneddata.csv"

# Paramètres de nettoyage des données
COLUMNS_TO_DROP = [
    'meta_users_number', 'meta_osm_url', 'meta_first_update', 'meta_last_update',
    'meta_versions_number', 'siret', 'wikidata', 'facebook'
]
