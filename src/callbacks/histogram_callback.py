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

        filtered_data['capacity_adjusted'] = filtered_data['capacity'].apply(lambda x: 1500 if x > 1500 else x)

        fig = px.histogram(
            filtered_data,
            x='capacity_adjusted',
            nbins=int(filtered_data['capacity_adjusted'].max() // 100),
            title='Distribution de la Capacité des Cinémas'
        )
        fig.update_traces(marker=dict(line=dict(width=1, color='black')), opacity=0.7)
        return fig