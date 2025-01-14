from dash import dcc, html

def create_map(valid_brands,regions):
    return html.Div([
                html.H2("Carte des Cinémas", style={'textAlign': 'center', 'marginBottom': '20px'}),
                html.Label("Filtrer par Marque :",style={'marginBottom': '7px', 'display': 'block'}),
                dcc.Dropdown(
                    id='map-marque-filter',
                    options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
                    value=None,
                    placeholder="Sélectionnez une marque",
                    style={ 'marginBottom': '10px'}
                ),
                html.Label("Filtrer par Région :",style={'marginBottom': '7px', 'display': 'block'}),
                dcc.Dropdown(
                    id='map-region-filter',
                    options=[{'label': region, 'value': region} for region in sorted(regions)],
                    value=None,
                    placeholder="Sélectionnez une région",
                    style={ 'marginBottom': '12px'}
                ),
                html.Div(id='map-container'),
            ])