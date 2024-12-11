import os
import pandas as pd

def cleaned_data(input_file: str, output_file: str) -> pd.DataFrame:
    # Charger les données brutes
    df = pd.read_csv(input_file, sep=';')

    # Supprimer les lignes avec des valeurs manquantes
    df_cleaned = df.dropna()

    # Supprimer les colonnes spécifiques
    columns_to_drop = ['href', 'href_formula', 'pdf', 'case_number']
    df_cleaned = df_cleaned.drop(columns=columns_to_drop, errors='ignore')  # errors='ignore' évite les erreurs si certaines colonnes n'existent pas

    # Vérifier si le répertoire de sortie existe, sinon le créer
    output_dir = os.path.dirname(output_file)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # Création du répertoire si nécessaire

    # Sauvegarder les données nettoyées dans le fichier
    df_cleaned.to_csv(output_file, index=False)

    return df_cleaned

# Appel de la fonction avec les chemins appropriés
cleaned_data('data/raw/dataset.csv', 'data/cleaned/cleaneddata.csv')
