import requests


def download_data(url: str, save_path: str) -> None:
    """
    Télécharge un fichier depuis une URL et le sauvegarde localement.

    Args:
        url (str): L'URL du fichier à télécharger.
        save_path (str): Chemin où sauvegarder le fichier téléchargé.
    """
    try:
        response = requests.get(url)

        with open(save_path, "wb") as file:
            file.write(response.content)

        print(f"Fichier téléchargé avec succès : {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")



dataset_url = "https://public.opendatasoft.com/explore/dataset/global-shark-attack/download/?format=csv"
save_location = "data/raw/dataset.csv"

download_data(dataset_url, save_location)

