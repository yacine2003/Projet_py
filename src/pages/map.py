from dash import dcc, html, dash
import pandas as pd
import numpy as np

def create_map(valid_brands: pd.Index, regions: np.ndarray) -> dash.html.Div :
    """
    Crée une mise en page pour afficher une carte interactive des cinémas,
    avec des options de filtrage par marque et par région.

    Args:
        valid_brands (pd.Index): Liste des marques valides à afficher dans le filtre.
        regions (np.ndarray): Liste des régions disponibles pour le filtre.

    Returns:
        dash.html.Div: Une mise en page Dash contenant des filtres et un conteneur pour la carte.
    """
    return html.Div([
        # Titre de la page
        html.H2("Carte des Cinémas", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Filtre par marque
        html.Label("Filtrer par Marque :", style={'marginBottom': '7px', 'display': 'block'}),
        dcc.Dropdown(
            id='map-marque-filter',
            options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
            value=None,
            placeholder="Sélectionnez une marque",
            style={'marginBottom': '10px'}
        ),
        
        # Filtre par région
        html.Label("Filtrer par Région :", style={'marginBottom': '7px', 'display': 'block'}),
        dcc.Dropdown(
            id='map-region-filter',
            options=[{'label': region, 'value': region} for region in sorted(regions)],
            value=None,
            placeholder="Sélectionnez une région",
            style={'marginBottom': '12px'}
        ),
        
        # Conteneur où la carte sera affichée dynamiquement
        html.Div(id='map-container'),
    ])
