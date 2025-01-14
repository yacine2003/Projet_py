from dash import html

def create_menu():
    return html.Div(
        [
            # Icône du menu
            html.Div(
                "☰",
                id='menu-icon',
                style={
                    'fontSize': '40px',
                    'cursor': 'pointer',
                    'padding': '10px',
                    'display': 'inline-block',
                    'position': 'fixed',
                    'top': '10px',
                    'left': '10px',
                    'zIndex': '1000',
                }
            ),

            # Menu latéral
            html.Div(
                id='side-menu',
                style={
                    'position': 'fixed',
                    'top': '0',
                    'left': '-250px',
                    'width': '250px',
                    'height': '100%',
                    'backgroundColor': '#333',
                    'color': 'white',
                    'padding': '0px',
                    'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
                    'transition': 'left 0.3s ease',
                    'zIndex': '999'
                },
                children=[
                    html.H2("Menu", style={'color': 'white','paddingTop':'40px'}),
                    html.Ul([
                        html.Li(html.A("Accueil", href="#", id='nav-accueil', style={'color': 'white', 'textDecoration': 'none','padding': '10px',})),
                        html.Li(html.A("Carte", href="#", id='nav-carte', style={'color': 'white', 'textDecoration': 'none','padding': '10px'})),
                        html.Li(html.A("Histogramme", href="#", id='nav-histogramme', style={'color': 'white', 'textDecoration': 'none','padding': '10px'}))
                    ],
                    style={
                        'listStyleType': 'none',  
                        'padding': '0',  
                        'margin': '0',  
                        'display': 'flex', 
                        'flexDirection': 'column',  
                        'gap': '15px'  
                    })
                ]
            )
        ],
        style={'position': 'relative'}
    )
