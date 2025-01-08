import os
import pandas as pd

def cleaned_data(input_file: str, output_file: str) -> pd.DataFrame:
    # Charger les données brutes
    df = pd.read_csv(input_file, sep=';')

    # Supprimer les colonnes spécifiques
    columns_to_drop = ['meta_users_number', 'meta_osm_url', 'meta_first_update', 'meta_last_update',
                       'meta_versions_number', 'siret', 'wikidata', 'facebook']
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')  # Ignore les erreurs si certaines colonnes n'existent pas

    # Supprimer les lignes où "capacity" est vide (NaN ou valeurs nulles)
    if 'capacity' in df_cleaned.columns:
        df_cleaned = df_cleaned.dropna(subset=['capacity'])

    # Vérifier si le répertoire de sortie existe, sinon le créer
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Création du répertoire si nécessaire

    # Sauvegarder les données nettoyées dans le fichier
    df_cleaned.to_csv(output_file, index=False)

    return df_cleaned

# Appel de la fonction avec les chemins appropriés
cleaned_data('data/raw/dataset.csv', 'data/cleaned/cleaneddata.csv')
