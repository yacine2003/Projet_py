import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
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

app.layout = html.Div([
    html.H1("Dashboard des Cinémas"),

    dcc.Tabs([
        # Carte
        dcc.Tab(label='Carte', children=[
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
        ]),

        # Histogramme
        dcc.Tab(label='Histogramme', children=[
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
    ])
])


# Callback pour mettre à jour l'histogramme
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
        filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]  # Utiliser meta_name_reg

    # Regrouper les cinémas avec une capacité supérieure à 1500 dans la tranche 1500
    filtered_data['capacity_adjusted'] = filtered_data['capacity'].apply(
        lambda x: 1500 if x > 1500 else x
    )

    # Histogramme de la capacité des cinémas avec des tranches de 100
    fig = px.histogram(
        filtered_data, 
        x='capacity_adjusted', 
        nbins=int(filtered_data['capacity_adjusted'].max() // 100),
        title='Distribution de la Capacité des Cinémas'
    )

    # Ajuster la largeur des barres et les délimiter plus clairement
    fig.update_traces(
        marker=dict(line=dict(width=1, color='black')),  # Délimiter les colonnes avec une bordure noire
        opacity=0.7,  # Rendre les colonnes légèrement transparentes pour plus de clarté
    )

    # Ajuster les axes pour zoomer et mieux délimiter
    fig.update_layout(
        xaxis=dict(
            title="Capacité",  # Titre de l'axe x
            range=[0, 1600],  # Limite de l'axe x pour un zoom (1500 + une petite marge)
            tickmode='array',  # Spécifier un mode de ticks pour plus de contrôle
            tickvals=list(range(0, 1600, 100)),  # Marquer les valeurs tous les 100 jusqu'à 1500
            showline=True,  # Afficher la ligne de l'axe
            zeroline=True,  # Afficher la ligne zéro
            zerolinecolor="black",  # Couleur de la ligne zéro
            zerolinewidth=2,  # Largeur de la ligne zéro
        ),
        yaxis=dict(
            title="Nombre de Cinémas",  # Titre de l'axe y
            range=[0, 400],  # Limiter l'axe y à 400
            showline=True,  # Afficher la ligne de l'axe
            zeroline=True,  # Afficher la ligne zéro
            zerolinecolor="black",  # Couleur de la ligne zéro
            zerolinewidth=2,  # Largeur de la ligne zéro
        ),
        bargap=0.1,  # Espacement entre les colonnes
        title_x=0.5,  # Centrer le titre
        title_y=0.95,  # Ajuster la position du titre
    )
    
    return fig


# Callback pour mettre à jour la carte Folium
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
        filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]  # Utiliser meta_name_reg

    # Créer la carte
    m = folium.Map(location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()], zoom_start=6)

    # Ajouter le cluster de marqueurs
    marker_cluster = MarkerCluster().add_to(m)

    # Ajouter les marqueurs pour chaque cinéma
    for _, row in filtered_data.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=(f"Nom: {row['name']}<br>"
                       f"Marque: {row['marque']}<br>"
                       f"Capacité: {row['capacity']}<br>"
                       f"Nombre d'écrans: {row['nb_screens']}")
            ).add_to(marker_cluster)

    map_html = m._repr_html_()

    return html.Iframe(srcDoc=map_html, width='100%', height='500')


if __name__ == '__main__':
    app.run_server(debug=True)
