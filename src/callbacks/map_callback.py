from dash import Input, Output, html, dash
import folium
import pandas as pd
from folium.plugins import MarkerCluster

def register_map_callbacks(app: dash.Dash, data: pd.DataFrame):
    """
    Enregistre un callback pour mettre à jour dynamiquement la carte en fonction des filtres 
    sélectionnés (marque et région).

    Args:
        app (dash.Dash): L'application Dash.
        data (pd.DataFrame): Les données contenant les informations sur les cinémas.
    """
    @app.callback(
        Output('map-container', 'children'),
        [
            Input('map-marque-filter', 'value'),
            Input('map-region-filter', 'value')
        ]
    )
    def update_map(selected_marque: str, selected_region: str) -> dash.html.Iframe:
        """
        Met à jour la carte en fonction des valeurs sélectionnées dans les filtres.

        Args:
            selected_marque (str): Marque sélectionnée dans le filtre.
            selected_region (str): Région sélectionnée dans le filtre.

        Returns:
            dash.html.Iframe: Une carte interactive Folium intégrée dans une iframe.
        """
        # Filtre les données en fonction des filtres
        filtered_data = data
        if selected_marque:
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
        if selected_region:
            filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

        # Vérification des données pour éviter les erreurs si elles sont vides
        if filtered_data.empty:
            return html.Div(
                "Aucune donnée disponible pour les filtres sélectionnés.",
                style={'textAlign': 'center', 'padding': '20px', 'color': 'red'}
            )

        # Créer une carte centrée sur la moyenne des coordonnées
        m = folium.Map(
            location=[filtered_data['latitude'].mean(), filtered_data['longitude'].mean()],
            zoom_start=6
        )

        # Ajout des marqueurs dans un cluster
        marker_cluster = MarkerCluster().add_to(m)
        for _, row in filtered_data.iterrows():
            if not pd.isna(row['latitude']) and not pd.isna(row['longitude']):
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=(f"Nom: {row['name']}<br>"
                           f"Marque: {row['marque']}<br>"
                           f"Capacité: {row['capacity']}<br>"
                           f"Nombre d'écrans: {row['nb_screens']}")
                ).add_to(marker_cluster)

        # Retourne la carte dans une iframe pour l'intégration dans Dash
        return html.Iframe(srcDoc=m._repr_html_(), width='100%', height='500px')



""" from dash import Input, Output, html
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

 """