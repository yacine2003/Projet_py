from dash import html, dash 

def create_home_page() -> dash.html.Div:
    """
    Génère la page d'accueil du tableau de bord.

    Returns:
        dash.html.Div: Une mise en page Dash.
    """
    return html.Div([
        # Titre principal
        html.H1(
            "Bienvenue dans le Dashboard des Cinémas", 
            style={'textAlign': 'center'}
        ),
        
        # Texte introductif
        html.P(
            "Utilisez le menu à gauche pour naviguer entre les sections.",
            style={'textAlign': 'center', 'fontSize': '18px'}
        ),
        
        # Description des fonctionnalités
        html.Div(
            "Ce tableau de bord vous permet de visualiser :", 
            style={'marginTop': '20px', 'fontSize': '16px'}
        ),
        
        # Liste des fonctionnalités
        html.Ul([
            html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
            html.Li("Un histogramme pour analyser la distribution des capacités."),
            html.Li("Une heatmap pour visualiser la densité des cinémas sur une région."),
        ], style={'fontSize': '16px'}),
    ])


