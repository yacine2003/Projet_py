import pandas as pd
import dash
from dash import html
from flask import Flask
from src.components.menu import create_menu
from src.callbacks.menu_callback import register_menu_callbacks
from src.callbacks.content_callback import register_content_callback
from src.callbacks.histogram_callback import register_histogram_callbacks
from src.callbacks.map_callback import register_map_callbacks
from src.callbacks.heatmap_callback import register_heatmap_callbacks
from src.callbacks.circle_callback import register_pie_chart_callbacks

from src.utils.get_data import download_data
from src.utils.clean_data import cleaned_data
from config import *

# Télécharger les données et les nettoyer

download_data(DATA_URL, RAW_DATA_PATH)
data = cleaned_data(RAW_DATA_PATH, CLEANED_DATA_PATH)


# Séparation des coordonnées de la colonne 'OSM Point' (latitude, longitude)
data[['latitude', 'longitude']] = data['meta_geo_point'].str.split(',', expand=True)
data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

# Filtrer les marques qui apparaissent au moins 5 fois
brand_counts = data['marque'].value_counts()
valid_brands = brand_counts[brand_counts >= 5].index
filtered_data = data[data['marque'].isin(valid_brands)]

# Créer une liste des régions à partir de la colonne 'meta_name_reg'
regions = data['meta_name_reg'].dropna().unique()

server = Flask(__name__)
app = dash.Dash(__name__, server=server, suppress_callback_exceptions=True)

app.layout = html.Div([
    create_menu(),
    # Conteneur principal pour le contenu affiché dynamiquement
    html.Div(id='main-content', style={'marginLeft': '0px', 'padding': '20px'})
])

# Enregistrement des callbacks
register_menu_callbacks(app)
register_content_callback(app,valid_brands,regions)
register_histogram_callbacks(app,data)
register_map_callbacks(app,data)
register_heatmap_callbacks(app, data)
register_pie_chart_callbacks(app, data)




if __name__ == '__main__':
    app.run_server(debug=True)

