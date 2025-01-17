from dash import Input, Output,dash
import plotly.express as px
import plotly
import pandas as pd

def register_histogram_callbacks(app: dash.Dash, data: pd.DataFrame):
    """
    Enregistre un callback pour mettre à jour dynamiquement l'histogramme en fonction
    des filtres sélectionnés

    Args:
        app (dash.Dash): L'application Dash.
        data (pd.DataFrame): Les données contenant les informations sur les cinémas
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
        Met à jour l'histogramme en fonction des valeurs sélectionnées dans les filtres

        Args:
            selected_marque (str): Marque sélectionnée dans le filtre
            selected_region (str): Région sélectionnée dans le filtre

        Returns:
            plotly.graph_objs._figure.Figure: Un graphique Plotly représentant l'histogramme
        """
        #filtre les données en fonction des filtres sélectionnés
        filtered_data = data
        if selected_marque:
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]
        if selected_region:
            filtered_data = filtered_data[filtered_data['meta_name_reg'] == selected_region]

        #ajuste les capacités pour limiter à 1500
        filtered_data['capacite'] = filtered_data['capacity'].apply(lambda x: 1500 if x > 1500 else x)

        fig = px.histogram(
            filtered_data,
            x='capacite',
            nbins=int(filtered_data['capacite'].max() // 100),
            title='Distribution de la Capacité des Cinémas',
            labels={'count': 'Nombre de cinémas', 'capacite': 'Capacité'}
        )

        #ajuster les barres pour inclure la colonne 1500+
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=0.7)

        tick_vals = list(range(0, 1599, 100)) + [1599]
        tick_texts = [f"{val}" for val in range(0, 1599, 100)] + ["1599+"]

        fig.update_layout(
            xaxis=dict(
                title="Capacité",
                tickmode="array",
                tickvals=tick_vals,
                ticktext=tick_texts,
            ),
            yaxis_title="Nombre de cinémas",
            title_x=0.5,
        )

        return fig
