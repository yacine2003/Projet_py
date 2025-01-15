from dash import Input, Output
import plotly.express as px

def register_histogram_callbacks(app, data):
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

        # Ajuster les capacités pour limiter à 1500
        filtered_data['capacite'] = filtered_data['capacity'].apply(lambda x: 1500 if x > 1500 else x)

        # Créer l'histogramme
        fig = px.histogram(
            filtered_data,
            x='capacite',
            nbins=int(filtered_data['capacite'].max() // 100),
            title='Distribution de la Capacité des Cinémas',
            labels={'count': 'Nombre de cinémas', 'capacite': 'Capacité'}
        )

        # Ajuster les barres pour inclure la colonne 1500+
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=0.7)

        # Personnalisation des ticks sur l'axe x
        tick_vals = list(range(0, 1599, 100)) + [1599]
        tick_texts = [f"{val}" for val in range(0, 1599, 100)] + ["1599+"]

        # Mise en page personnalisée
        fig.update_layout(
            xaxis=dict(
                title="Capacité",
                tickmode="array",
                tickvals=tick_vals,
                ticktext=tick_texts,
            ),
            yaxis_title="Nombre de cinémas",
            title_x=0.5,  # Centrer le titre
        )

        return fig
