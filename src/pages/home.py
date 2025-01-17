import dash
from dash import html

def create_home_page() -> dash.html.Div:
    """
    Génère la page d'accueil du tableau de bord

    Returns:
        dash.html.Div: Une mise en page Dash
    """
    return html.Div([
        #titre principal
        html.H1(
            "Bienvenue dans le Dashboard des Cinémas en France", 
            style={'textAlign': 'center'}
        ),
        
        #texte introductif
        html.P(
            "Utilisez le menu à gauche pour naviguer entre les sections.",
            style={'textAlign': 'center', 'fontSize': '22px'}
        ),
        
        #description des fonctionnalités
        html.Div(
            "Ce tableau de bord vous permet de visualiser :", 
            style={'marginTop': '20px', 'fontSize': '20px'}
        ),
        
        #liste des fonctionnalité
        html.Ul([
            html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
            html.Li("Un histogramme pour analyser la distribution des capacités."),
            html.Li("Une heatmap pour visualiser la densité des cinémas."),
            html.Li("Un diagramme circulaire de la répartition des cinémas par régions."),
        ], style={'fontSize': '20px'}),
    ])


