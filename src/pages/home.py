from dash import html

def create_home_page():
    return html.Div([
            html.H1("Bienvenue dans le Dashboard des Cinémas en France", style={'textAlign': 'center'}),
            html.P(
                "Utilisez le menu à gauche pour naviguer entre les sections.",
                style={'textAlign': 'center', 'fontSize': '18px'}
            ),
            html.Div(
                "Ce tableau de bord vous permet de visualiser :",
                style={'marginTop': '20px', 'fontSize': '16px'}
            ),
            html.Ul([
                html.Li("Une carte interactive des cinémas et de leurs caractéristiques."),
                html.Li("Un histogramme pour analyser la distribution des capacités."),
                html.Li("Une carte de chaleur pour visualier la répartition des cinémas en france."),
                html.Li("Un digramme circulaire pour montrer la répartition des cinémas par régions."),
            ], style={'fontSize': '16px'}),
        ])




