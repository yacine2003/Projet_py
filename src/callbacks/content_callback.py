from dash import Input, Output, callback_context
import dash
from src.pages.home import create_home_page
from src.pages.map import create_map
from src.pages.histogram import create_histogram
from src.pages.heatmap import create_heatmap

def register_content_callback(app, valid_brands, regions):
    @app.callback(
        Output('main-content', 'children'),
        [
            Input('nav-accueil', 'n_clicks'),
            Input('nav-carte', 'n_clicks'),
            Input('nav-histogramme', 'n_clicks'),
            Input('nav-carteheat', 'n_clicks')
            
        ]
    )

    def display_content(nav_accueil_clicks, nav_carte_clicks, nav_histogramme_clicks,nav_carteheat_clicks ):
        # Obtenir le contexte du déclencheur
        ctx = dash.callback_context

        # Si aucun lien n'a été cliqué, afficher la page d'accueil par défaut
        if not ctx.triggered:
            return create_home_page()

        # Identifier quel lien a été cliqué
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        if triggered_id == 'nav-accueil':
            return create_home_page()

        elif triggered_id == 'nav-carte':
            return create_map(valid_brands,regions)

        elif triggered_id == 'nav-histogramme':
            return create_histogram(valid_brands,regions)
        
        elif triggered_id == 'nav-carteheat':
            return create_heatmap(valid_brands,regions)


