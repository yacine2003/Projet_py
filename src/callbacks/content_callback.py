from dash import Input, Output, callback_context
import dash,numpy as np, pandas as pd
from src.pages.home import create_home_page
from src.pages.map import create_map
from src.pages.histogram import create_histogram
from src.pages.heatmap import create_heatmap
from src.pages.circle import create_pie_chart

def register_content_callback(app: dash.Dash, valid_brands: pd.Index, regions: np.ndarray):
    """
    Enregistre un callback pour mettre à jour dynamiquement le contenu de la section principale 
    ('main-content') en fonction du menu cliqué.

    Args:
        app (dash.Dash): L'application Dash.
        valid_brands (pd.Index): Index des marques valides à afficher.
        regions (np.ndarray): Tableau des régions disponibles pour le filtre.
    """
    @app.callback(
        Output('main-content', 'children'),
        [
            Input('nav-accueil', 'n_clicks'),
            Input('nav-carte', 'n_clicks'),
            Input('nav-histogramme', 'n_clicks'),
            Input('nav-carteheat', 'n_clicks'),
            Input('nav-circle', 'n_clicks'),
            
        ]
    )



    def display_content(nav_accueil_clicks: int, nav_carte_clicks: int, nav_histogramme_clicks: int, nav_carteheat_clicks: int) -> dash.html.Div:
        """
        Gère les clics sur les liens du menu et met à jour le contenu affiché dans 'main-content'.

        Args:
            nav_accueil_clicks (int): Nombre de clics sur le lien "Accueil".
            nav_carte_clicks (int): Nombre de clics sur le lien "Carte".
            nav_histogramme_clicks (int): Nombre de clics sur le lien "Histogramme".

        Returns:
            dash.html.Div: Le contenu correspondant à la page sélectionnée.
        """
        # Obtient le contexte du déclencheur
        ctx = callback_context

        # Si aucun lien n'a été cliqué, on affiche la page d'accueil par défaut

        if not ctx.triggered:
            return create_home_page()

        # Identifie quel lien a été cliqué
        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

        # Logique pour afficher la page appropriée
        if triggered_id == 'nav-accueil':
            return create_home_page()
        elif triggered_id == 'nav-carte':
            return create_map(valid_brands, regions)
        elif triggered_id == 'nav-histogramme':
            return create_histogram(valid_brands,regions)
        
        elif triggered_id == 'nav-carteheat':
            return create_heatmap(valid_brands,regions)
        
        elif triggered_id == 'nav-circle':
            return create_pie_chart(valid_brands, regions)



