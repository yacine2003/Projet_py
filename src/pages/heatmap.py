from dash import dcc, html

def create_heatmap(valid_brands,regions):
    """
    Crée l'interface utilisateur pour afficher une carte de chaleur des cinémas, avec des filtres interactifs 
    pour la sélection de la marque et de la région

    Args:
        valid_brands (list): Liste des marques de cinémas disponibles pour filtrer les données sur la carte de chaleur
        regions (list): Liste des régions disponibles pour filtrer les données sur la carte de chaleur

    Returns:
        html.Div: Un composant HTML contenant l'interface utilisateur pour la carte de chaleur, y compris 
                  des filtres sous forme de dropdowns pour sélectionner la marque et la région
    """
    return html.Div([
        html.H2("Carte de Chaleur des Cinémas", style={'textAlign': 'center', 'marginBottom': '20px'}),
        html.Label("Filtrer par Marque :", style={'marginBottom': '7px', 'display': 'block'}),
        dcc.Dropdown(
            id='heatmap-marque-filter',
            options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
            value=None,
            placeholder="Sélectionnez une marque",
            style={'marginBottom': '10px'}
        ),
        html.Label("Filtrer par Région :", style={'marginBottom': '7px', 'display': 'block'}),
        dcc.Dropdown(
            id='heatmap-region-filter',
            options=[{'label': region, 'value': region} for region in sorted(regions)],
            value=None,
            placeholder="Sélectionnez une région",
            style={'marginBottom': '12px'}
        ),
        html.Div(id='heatmap-container'),
    ])



