from dash import Input, Output, html
import folium
from folium.plugins import HeatMap

def register_heatmap_callbacks(app, data):
    """
    Enregistre les callbacks pour générer et afficher une carte de chaleur dans l'application Dash.
    Cette fonction est responsable de la mise à jour de la carte de chaleur chaque fois que l'utilisateur applique 
    un filtre sur la marque ou la région.

    Args:
        app (dash.Dash): L'instance de l'application Dash.
        data (pandas.DataFrame): Le DataFrame contenant les données des cinémas, y compris les informations 
                                  sur la latitude, la longitude, la marque, et la région des cinémas.

    Returns:
        None: La fonction enregistre un callback pour mettre à jour la carte de chaleur, mais ne retourne rien directement.
    """
    @app.callback(
        Output('heatmap-container', 'children'),
        [
            Input('heatmap-marque-filter', 'value'),
            Input('heatmap-region-filter', 'value')
        ]
    )
    def update_heatmap(selected_marque, selected_region):
        """
        Met à jour la carte de chaleur en fonction des filtres de marque et de région appliqués par l'utilisateur.

        Args:
            selected_marque (str or None): La marque de cinéma sélectionnée dans le filtre. Si aucun filtre n'est appliqué, 
                                            cette valeur sera `None`.
            selected_region (str or None): La région sélectionnée dans le filtre. Si aucun filtre n'est appliqué, 
                                           cette valeur sera `None`.

        Returns:
            html.Iframe: Un objet html.Iframe contenant la carte de chaleur générée par Folium.
        """
        filtered_data = data
        if selected_marque:
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
        if selected_region:
            filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

        heat_data = filtered_data[['latitude', 'longitude']].dropna().values.tolist()

        # Créer une carte centrée sur la France
        m = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

        HeatMap(heat_data, radius=15, blur=10).add_to(m)

        return html.Iframe(srcDoc=m._repr_html_(), width='100%', height='500')
