import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
from flask import Flask

# Charger les données
data = pd.read_csv('data/cleaned/cleaneddata.csv')

# Séparation des coordonnées de la colonne 'OSM Point' (latitude, longitude)
data[['latitude', 'longitude']] = data['meta_geo_point'].str.split(',', expand=True)
data['latitude'] = pd.to_numeric(data['latitude'], errors='coerce')
data['longitude'] = pd.to_numeric(data['longitude'], errors='coerce')

# Filtrer les marques qui apparaissent au moins 5 fois
brand_counts = data['marque'].value_counts()
valid_brands = brand_counts[brand_counts >= 5].index
filtered_data = data[data['marque'].isin(valid_brands)]

# Créer une liste des régions à partir de la colonne 'meta_name_reg'
regions = data['meta_name_reg'].dropna().unique()  # Utiliser la colonne meta_name_reg pour les régions

# Config dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

# Définir la mise en page
app.layout = html.Div([
    # Conteneur pour l'icône du menu et le menu latéral
    html.Div(
        [
            # Icône du menu
            html.Div(
                "☰",
                id='menu-icon',
                style={
                    'fontSize': '40px',
                    'cursor': 'pointer',
                    'padding': '10px',
                    'display': 'inline-block',
                    'position': 'fixed',
                    'top': '10px',
                    'left': '10px',
                    'zIndex': '1000',
                }
            ),

            # Menu latéral
            html.Div(
                id='side-menu',
                style={
                    'position': 'fixed',
                    'top': '0',
                    'left': '-250px',
                    'width': '250px',
                    'height': '100%',
                    'backgroundColor': '#333',
                    'color': 'white',
                    'padding': '0px',
                    'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
                    'transition': 'left 0.3s ease',
                    'zIndex': '999'
                },
                children=[
                    html.H2("Menu", style={'color': 'white','padding-top':'40px'}),
                    html.Ul([
                        html.Li(html.A("Accueil", href="#", id='nav-accueil', style={'color': 'white', 'textDecoration': 'none','padding': '10px',})),
                        html.Li(html.A("Carte", href="#", id='nav-carte', style={'color': 'white', 'textDecoration': 'none','padding': '10px'})),
                        html.Li(html.A("Histogramme", href="#", id='nav-histogramme', style={'color': 'white', 'textDecoration': 'none','padding': '10px'}))
                    ],
                    style={
                        'listStyleType': 'none',  
                        'padding': '0',  
                        'margin': '0',  
                        'display': 'flex', 
                        'flexDirection': 'column',  
                        'gap': '15px'  
                    })
                ]
            )
        ],
        style={'position': 'relative'}
    ),

    # Conteneur principal pour le contenu affiché dynamiquement
    html.Div(id='main-content', style={'marginLeft': '0px', 'padding': '20px'})
])

# Callback pour afficher/masquer le menu
@app.callback(
    Output('side-menu', 'style'),
    Input('menu-icon', 'n_clicks'),
    prevent_initial_call=True
)
def toggle_menu(n_clicks):
    if n_clicks % 2 == 1:
        return {
            'position': 'fixed',
            'top': '15',
            'left': '0',
            'width': '250px',
            'height': '100%',
            'backgroundColor': '#333',
            'color': 'white',
            'padding': '15px',
            'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
            'transition': 'left 0.3s ease',
            'zIndex': '999'
        }
    else:
        return {
            'position': 'fixed',
            'top': '0',
            'left': '-1000px',
            'width': '250px',
            'height': '100%',
            'backgroundColor': '#333',
            'color': 'white',
            'padding': '0px',
            'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
            'transition': 'left 0.3s ease',
            'zIndex': '999'
        }



@app.callback(
    Output('main-content', 'children'),
    [
        Input('nav-accueil', 'n_clicks'),
        Input('nav-carte', 'n_clicks'),
        Input('nav-histogramme', 'n_clicks')
    ]
)

def display_content(nav_accueil_clicks, nav_carte_clicks, nav_histogramme_clicks):
    # Obtenir le contexte du déclencheur
    ctx = dash.callback_context

    # Si aucun lien n'a été cliqué, afficher la page d'accueil par défaut
    if not ctx.triggered:
        return html.Div([
            html.H1("Bienvenue dans le Dashboard des Cinémas", style={'textAlign': 'center'}),
            html.P(
                "Utilisez le menu à gauche pour naviguer entre les sections.",
                style={'textAlign': 'center', 'fontSize': '18px'}
            ),
            html.Div(
                "Ce tableau de bord vous permet de visualiser :",
                style={'marginTop': '20px', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
                html.Li("Un histogramme pour analyser la distribution des capacités."),
            ], style={'fontSize': '16px'}),
        ])

    # Identifier quel lien a été cliqué
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'nav-accueil':
        # Afficher la page d'accueil
        return html.Div([
            html.H1("Bienvenue dans le Dashboard des Cinémas", style={'textAlign': 'center'}),
            html.P(
                "Utilisez le menu à gauche pour naviguer entre les sections.",
                style={'textAlign': 'center', 'fontSize': '18px'}
            ),
            html.Div(
                "Ce tableau de bord vous permet de visualiser :",
                style={'marginTop': '20px', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
                html.Li("Un histogramme pour analyser la distribution des capacités."),
            ], style={'fontSize': '16px'}),
        ])

    elif triggered_id == 'nav-carte':
        # Afficher la section Carte avec un titre
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

    elif triggered_id == 'nav-histogramme':
        # Afficher la section Histogramme avec un titre
        return html.Div([
            html.H2("Analyse des Capacités des Cinémas", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.Label("Filtrer par Marque :",style={'marginBottom': '7px', 'display': 'block'}),
            dcc.Dropdown(
                id='hist-marque-filter',
                options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
                value=None,
                placeholder="Sélectionnez une marque",
                style={ 'marginBottom': '10px'}
            ),
            html.Label("Filtrer par Région :",style={'marginBottom': '7px', 'display': 'block'}),
            dcc.Dropdown(
                id='hist-region-filter',
                options=[{'label': region, 'value': region} for region in sorted(regions)],
                value=None,
                placeholder="Sélectionnez une région",
                style={ 'marginBottom': '12px'}
            ),
            dcc.Graph(id='histogram'),
        ])
""" def display_content(nav_accueil_clicks, nav_carte_clicks, nav_histogramme_clicks):
    # Obtenir le contexte du déclencheur
    ctx = dash.callback_context

    # Si aucun lien n'a été cliqué, afficher la page d'accueil par défaut
    if not ctx.triggered:
        return html.Div([
            html.H1("Bienvenue dans le Dashboard des Cinémas", style={'textAlign': 'center'}),
            html.P(
                "Utilisez le menu à gauche pour naviguer entre les sections.",
                style={'textAlign': 'center', 'fontSize': '18px'}
            ),
            html.Div(
                "Ce tableau de bord vous permet de visualiser :",
                style={'marginTop': '20px', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
                html.Li("Un histogramme pour analyser la distribution des capacités."),
            ], style={'fontSize': '16px'}),
        ])

    # Identifier quel lien a été cliqué
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if triggered_id == 'nav-accueil':
        # Afficher la page d'accueil
        return html.Div([
            html.H1("Bienvenue dans le Dashboard des Cinémas", style={'textAlign': 'center'}),
            html.P(
                "Utilisez le menu à gauche pour naviguer entre les sections.",
                style={'textAlign': 'center', 'fontSize': '18px'}
            ),
            html.Div(
                "Ce tableau de bord vous permet de visualiser :",
                style={'marginTop': '20px', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
                html.Li("Un histogramme pour analyser la distribution des capacités."),
            ], style={'fontSize': '16px'}),
        ])

    elif triggered_id == 'nav-carte':
        # Afficher la section Carte
        return html.Div([
            html.Label("Filtrer par Marque :"),
            dcc.Dropdown(
                id='map-marque-filter',
                options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
                value=None,
                placeholder="Sélectionnez une marque"
            ),
            html.Label("Filtrer par Région :"),
            dcc.Dropdown(
                id='map-region-filter',
                options=[{'label': region, 'value': region} for region in sorted(regions)],
                value=None,
                placeholder="Sélectionnez une région"
            ),
            html.Div(id='map-container'),
        ])

    elif triggered_id == 'nav-histogramme':
        # Afficher la section Histogramme
        return html.Div([
            html.Label("Filtrer par Marque :"),
            dcc.Dropdown(
                id='hist-marque-filter',
                options=[{'label': marque, 'value': marque} for marque in sorted(valid_brands)],
                value=None,
                placeholder="Sélectionnez une marque"
            ),
            html.Label("Filtrer par Région :"),
            dcc.Dropdown(
                id='hist-region-filter',
                options=[{'label': region, 'value': region} for region in sorted(regions)],
                value=None,
                placeholder="Sélectionnez une région"
            ),
            dcc.Graph(id='histogram'),
        ])
 """


# Callback pour l'histogramme
@app.callback(
    Output('histogram', 'figure'),
    [
        Input('hist-marque-filter', 'value'),
        Input('hist-region-filter', 'value')
    ]
)
def update_histogram(selected_marque, selected_region):
    filtered_data = data
    if selected_marque:
        filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
    if selected_region:
        filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

    filtered_data['capacity_adjusted'] = filtered_data['capacity'].apply(lambda x: 1500 if x > 1500 else x)

    fig = px.histogram(
        filtered_data,
        x='capacity_adjusted',
        nbins=int(filtered_data['capacity_adjusted'].max() // 100),
        title='Distribution de la Capacité des Cinémas'
    )
    fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=0.7)
    return fig

# Callback pour la carte
@app.callback(
    Output('map-container', 'children'),
    [
        Input('map-marque-filter', 'value'),
        Input('map-region-filter', 'value')
    ]
)
def update_map(selected_marque, selected_region):
    filtered_data = data
    if selected_marque:
        filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
    if selected_region:
        filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in filtered_data.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=(f"Nom: {row['name']}<br>Marque: {row['marque']}<br>Capacité: {row['capacity']}<br>Nombre d'écrans: {row['nb_screens']}")
            ).add_to(marker_cluster)

    return html.Iframe(srcDoc=m._repr_html_(), width='100%', height='500')


if __name__ == '__main__':
    app.run_server(debug=True)
