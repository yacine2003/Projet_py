import requests


def download_data(url: str, save_path: str) -> None:
    """
    Télécharge un fichier depuis une URL et le sauvegarde localement.

    Args:
        url (str): L'URL du fichier à télécharger.
        save_path (str): Chemin où sauvegarder le fichier téléchargé.

    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Vérifie si la requête a réussi 

        with open(save_path, "wb") as file:
            file.write(response.content)

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors du téléchargement : {e}")
        raise e


