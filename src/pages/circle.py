from dash import dcc, html

def create_pie_chart(valid_brands, regions):
    """
    Crée l'interface utilisateur avec des filtres pour afficher un diagramme circulaire de la répartition des cinémas
    par région avec un filtre supplémentaire pour les marques
    
    Args:
        valid_brands (list): Liste des marques de cinémas disponibles
        regions (list): Liste des régions disponibles pour filtrer les données
    
    Returns:
        html.Div: Le composant contenant le diagramme circulaire et les filtres
    """
    return html.Div([
        html.H2("Diagramme circulaire de la répartition des Cinémas par Région", style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        html.Label("Filtrer par Marque :", style={'marginBottom': '7px', 'display': 'block'}),
        dcc.Dropdown(
            id='pie-chart-marque-filter',
            options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
            value=None,
            placeholder="Sélectionnez une marque",
            style={'marginBottom': '10px'}
        ),
        
        html.Div(id='pie-chart-container'),
    ])
