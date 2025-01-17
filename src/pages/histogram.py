from dash import html, dcc, dash
import pandas as pd
import numpy as np

def create_histogram(valid_brands: pd.Index, regions: np.ndarray) -> dash.html.Div:
    """
    Crée une mise en page pour afficher un histogramme des capacités des cinémas,
    avec des options de filtrage par marque et par région

    Args:
        valid_brands (pd.Index or list): Index ou liste contenant les marques valides
        regions (np.ndarray or list): Tableau ou liste des régions disponibles pour le filtre

    Returns:
        dash.html.Div: Une mise en page Dash contenant des filtres et un graphique
    """
    #convertir valid_brands et regions en listes si nécessaire
    valid_brands_list = valid_brands.tolist() if hasattr(valid_brands, 'tolist') else list(valid_brands)
    regions_list = regions.tolist() if hasattr(regions, 'tolist') else list(regions)

    return html.Div([
        #titre principal
        html.H2(
            "Analyse des Capacités des Cinémas", 
            style={'textAlign': 'center', 'marginBottom': '20px'}
        ),

        #filtre par marque
        html.Label(
            "Filtrer par Marque :", 
            style={'marginBottom': '7px', 'display': 'block'}
        ),
        dcc.Dropdown(
            id='hist-marque-filter',
            options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands_list)],
            value=None,
            placeholder="Sélectionnez une marque",
            style={'marginBottom': '10px'}
        ),

        #filtre par région
        html.Label(
            "Filtrer par Région :", 
            style={'marginBottom': '7px', 'display': 'block'}
        ),
        dcc.Dropdown(
            id='hist-region-filter',
            options=[{'label': region, 'value': region} for region in sorted(regions_list)],
            value=None,
            placeholder="Sélectionnez une région",
            style={'marginBottom': '12px'}
        ),

        dcc.Graph(id='histogram'),
    ])
