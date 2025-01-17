import os
import pandas as pd

def cleaned_data(input_file: str, output_file: str) -> pd.DataFrame:
    """
    Nettoie les données en supprimant des colonnes inutiles et des lignes avec des valeurs manquantes dans une colonne clé,
    puis sauvegarde le fichier nettoyé dans un chemin donné

    Args:
        input_file (str): Chemin du fichier CSV d'entrée contenant les données brutes
        output_file (str): Chemin où sauvegarder le fichier CSV des données nettoyées

    Returns:
        pd.DataFrame: Un DataFrame contenant les données nettoyées
    """
    try:
        df = pd.read_csv(input_file, sep=';')

        #supprimer les colonnes spécifiques
        columns_to_drop = ['meta_users_number', 'meta_osm_url', 'meta_first_update', 'meta_last_update',
                           'meta_versions_number', 'siret', 'wikidata', 'facebook']
        df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')  #ignore les erreurs si certaines colonnes n'existent pas

        #suppression des lignes où "capacity" est vide
        if 'capacity' in df_cleaned.columns:
            df_cleaned = df_cleaned.dropna(subset=['capacity'])

        output_dir = os.path.dirname(output_file)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        df_cleaned.to_csv(output_file, index=False)

        return df_cleaned

    except FileNotFoundError as e:
        print(f"Erreur : Fichier d'entrée non trouvé ({input_file}).")
        raise e

