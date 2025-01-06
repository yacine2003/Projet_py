import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import folium
from flask import Flask

from src.utils.dict_coordonnees import dict_coord

data = pd.read_csv('data/cleaned/cleaneddata.csv')

# Assurer que les clés sont bien converties en type attendu
data['original_order'] = data['original_order'].astype(str)

# Préparer les coordonnées pour fusion avec les données
coordinates_df = pd.DataFrame.from_dict(dict_coord, orient='index', columns=['latitude', 'longitude'])
coordinates_df.index.name = 'original_order'
coordinates_df.reset_index(inplace=True)

# Fusion coordonnées avec les données de base
data = pd.merge(data, coordinates_df, on='original_order', how='left')

#Config dash
server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    html.H1("Dashboard des Attaques de Requins"),

    dcc.Tabs([
        dcc.Tab(label='Carte', children=[
            html.Label("Filtrer par année :"),
            dcc.Dropdown(
                id='map-year-filter',
                options=[{'label': year, 'value': year} for year in sorted(data['year'].dropna().unique())],
                value=None,
                placeholder="Sélectionnez une année"
            ),

            html.Label("Filtrer par pays :"),
            dcc.Dropdown(
                id='map-country-filter',
                options=[{'label': country, 'value': country} for country in sorted(data['country'].dropna().unique())],
                value=None,
                placeholder="Sélectionnez un pays"
            ),

            html.Div(id='map-container'),
        ]),
        
        dcc.Tab(label='Histogramme', children=[
            html.Label("Filtrer par année :"),
            dcc.Dropdown(
                id='hist-year-filter',
                options=[{'label': year, 'value': year} for year in sorted(data['year'].dropna().unique())],
                value=None,
                placeholder="Sélectionnez une année"
            ),

            html.Label("Filtrer par pays :"),
            dcc.Dropdown(
                id='hist-country-filter',
                options=[{'label': country, 'value': country} for country in sorted(data['country'].dropna().unique())],
                value=None,
                placeholder="Sélectionnez un pays"
            ),

            dcc.Graph(id='histogram'),
        ])
    ])
])

# Callback pour mettre à jour les options des Dropdowns dynamiquement pour la carte
@app.callback(
    [
        Output('map-year-filter', 'options'),
        Output('map-country-filter', 'options')
    ],
    [
        Input('map-year-filter', 'value'),
        Input('map-country-filter', 'value')
    ]
)
def update_map_dropdown_options(selected_year, selected_country):
    filtered_data = data
    
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == selected_year]

    year_options = [{'label': year, 'value': year} for year in sorted(filtered_data['year'].dropna().unique())]
    country_options = [{'label': country, 'value': country} for country in sorted(filtered_data['country'].dropna().unique())]

    return year_options, country_options

# Callback pour mettre à jour les options des Dropdowns dynamiquement pour l'histogramme
@app.callback(
    [
        Output('hist-year-filter', 'options'),
        Output('hist-country-filter', 'options')
    ],
    [
        Input('hist-year-filter', 'value'),
        Input('hist-country-filter', 'value')
    ]
)
def update_hist_dropdown_options(selected_year, selected_country):
    filtered_data = data
    
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == selected_year]

    year_options = [{'label': year, 'value': year} for year in sorted(filtered_data['year'].dropna().unique())]
    country_options = [{'label': country, 'value': country} for country in sorted(filtered_data['country'].dropna().unique())]

    return year_options, country_options

# Callback pour mettre à jour l'histogramme
@app.callback(
    Output('histogram', 'figure'),
    [
        Input('hist-year-filter', 'value'),
        Input('hist-country-filter', 'value')
    ]
)
def update_histogram(selected_year, selected_country):
    filtered_data = data
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == selected_year]
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    fig = px.histogram(filtered_data, x='year', title='Nombre d\'attaques par année')
    return fig

# Callback pour mettre à jour la carte Folium
@app.callback(
    Output('map-container', 'children'),
    [
        Input('map-year-filter', 'value'),
        Input('map-country-filter', 'value')
    ]
)
def update_map(selected_year, selected_country):
    filtered_data = data
    if selected_year:
        filtered_data = filtered_data[filtered_data['year'] == selected_year]
    if selected_country:
        filtered_data = filtered_data[filtered_data['country'] == selected_country]

    # Zoom sur le pays sélectionné
    if selected_country and not filtered_data.empty:
        country_data = filtered_data[filtered_data['country'] == selected_country]
        avg_lat = country_data['latitude'].mean()
        avg_lon = country_data['longitude'].mean()
        m = folium.Map(location=[avg_lat, avg_lon], zoom_start=5)
    else:
        m = folium.Map(location=[0, 0], zoom_start=2)

    # Ajout des marqueurs sur la carte
    for _, row in filtered_data.iterrows():
        if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=(
                    f"Lieu: {row['location']}<br>"
                    f"Année: {row['year']}<br>"
                    f"Espèce: {row['species']}<br>"
                    f"Blessure: {row['injury']}<br>"
                    f"Âge: {row.get('age', 'Inconnu')}"
                )
            ).add_to(m)

    map_html = m._repr_html_()

    return html.Iframe(srcDoc=map_html, width='100%', height='500')

if __name__ == '__main__':
    app.run_server(debug=True)




