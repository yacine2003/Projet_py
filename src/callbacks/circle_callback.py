from dash import Input, Output, dcc, html
import plotly.express as px

def register_pie_chart_callbacks(app, data):
    """
    Enregistre le callback pour mettre à jour le diagramme circulaire en fonction des filtres de marque et de région
    
    Args:
        app (dash.Dash): L'instance de l'application Dash
        data (pandas.DataFrame): Le DataFrame contenant les informations des cinémas, y compris les marques et les régions
        
    Returns:
        None: Le callback met à jour le diagramme circulaire et ne retourne rien directement
    """
    @app.callback(
        Output('pie-chart-container', 'children'),
        [
            Input('pie-chart-marque-filter', 'value'),
        ]
    )
    def update_pie_chart(selected_marque):
        """
        Met à jour le diagramme circulaire en fonction des filtres de marque et de région appliqués par l'utilisateur
        
        Args:
            selected_marque (str or None): La marque de cinéma sélectionnée dans le filtre. Si aucun filtre n'est appliqué None
        
        Returns:
            plotly.graph_objects.Figure: Le diagramme circulaire représentant la répartition des cinémas par région
        """
        filtered_data = data
        if selected_marque:
            filtered_data = filtered_data[filtered_data['marque'] == selected_marque]

        region_counts = filtered_data['meta_name_reg'].value_counts().reset_index()
        region_counts.columns = ['Région', 'Nombre de Cinémas']
        
        fig = px.pie(region_counts, 
                     names='Région', 
                     values='Nombre de Cinémas', 
                     title="Répartition des Cinémas par Région")
        
        return dcc.Graph(figure=fig)
