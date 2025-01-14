from dash import Input, Output, html
import folium, pandas as pd
from folium.plugins import MarkerCluster

def register_map_callbacks(app,data):
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

