import csv
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Initialiser le géocodeur
geolocator = Nominatim(user_agent="geo_locator")

# Fonction pour récupérer les coordonnées
def get_coordinates(location_name):
    try:
        location = geolocator.geocode(location_name, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None

# Chemin du fichier d'entrée
input_file = "data/cleaned/cleaneddata.csv"  # Remplacez par votre chemin

# Dictionnaire pour stocker les coordonnées
coordinates_dict = {}

# Lire le fichier CSV et extraire les coordonnées
with open(input_file, mode='r', encoding='utf-8') as infile:

    reader = csv.DictReader(infile)

    for row in reader:
        original_order = row['original_order']  # Identifiant unique

        # Essayer successivement Location, Area, puis Country
        latitude, longitude = None, None
        for column in ['location', 'area', 'country']:
            if not latitude and not longitude and row[column]:
                print(column)
                latitude, longitude = get_coordinates(row[column])

        # Ajouter les coordonnées dans le dictionnaire
        coordinates_dict[original_order] = (latitude, longitude)

# Imprimer le dictionnaire des coordonnées
print("Dictionnaire des coordonnees :")
print(coordinates_dict)

