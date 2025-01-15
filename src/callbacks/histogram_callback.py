from dash import Input, Output,dash
import plotly.express as px
import plotly
import pandas as pd

def register_histogram_callbacks(app: dash.Dash, data: pd.DataFrame):
    """
    Enregistre un callback pour mettre à jour dynamiquement l'histogramme en fonction
    des filtres sélectionnés.

    Args:
        app (dash.Dash): L'application Dash.
        data (pd.DataFrame): Les données contenant les informations sur les cinémas.
    """
    @app.callback(
        Output('histogram', 'figure'),
        [
            Input('hist-marque-filter', 'value'),
            Input('hist-region-filter', 'value')
        ]
    )
    def update_histogram(selected_marque: str, selected_region: str) -> plotly.graph_objs._figure.Figure:
        """
        Met à jour l'histogramme en fonction des valeurs sélectionnées dans les filtres.

        Args:
            selected_marque (str): Marque sélectionnée dans le filtre.
            selected_region (str): Région sélectionnée dans le filtre.

        Returns:
            plotly.graph_objs._figure.Figure: Un graphique Plotly représentant l'histogramme.
        """
        # Filtre les données en fonction des filtres sélectionnés
        filtered_data = data
        if selected_marque:
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
        if selected_region:
            filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

        # Vérifie si la colonne 'capacity' existe et ajuste les valeurs
        if 'capacity' in filtered_data.columns:
            filtered_data['capacity_adjusted'] = filtered_data['capacity'].apply(lambda x: min(x, 1500))
        else:
            raise ValueError("La colonne 'capacity' est manquante dans les données.")

        # Créer l'histogramme avec Plotly
        fig = px.histogram(
            filtered_data,
            x='capacity_adjusted',
            nbins=20,
            title='Distribution de la Capacité des Cinémas'
        )
        fig.update_traces(
            marker=dict(line=dict(width=1, color='black')),
            opacity=0.7
        )

        return fig