from dash import html, dash

def create_menu() -> dash.html.Div:
    """
    Crée un menu latéral interactif avec une icône pour l'afficher ou le masquer

    Returns:
        dash.html.Div: Composant HTML contenant le menu latéral et l'icône associée
    """
    return html.Div(
        [
            #icone du menu
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

            #menu latéral
            html.Div(
                id='side-menu',
                style={
                    'position': 'fixed',
                    'top': '0',
                    'left': '-250px',  #menu caché par défaut
                    'width': '250px',
                    'height': '100%',
                    'backgroundColor': '#333',
                    'color': 'white', 
                    'padding': '0px',
                    'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
                    'transition': 'left 0.3s ease',  #transition fluide
                    'zIndex': '999'  #assure que le menu est au-dessus des autres éléments
                },
                children=[

                    html.H2(
                        "Menu", 
                        style={
                            'color': 'white', 
                            'paddingTop': '40px', 
                            'textAlign': 'center'
                        }
                    ),

                    #liens du menu
                    html.Ul(
                        [
                            html.Li(
                                html.A(
                                    "Accueil", 
                                    href="#", 
                                    id='nav-accueil', 
                                    style={
                                        'color': 'white', 
                                        'textDecoration': 'none',
                                        'padding': '10px',
                                    }
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Carte", 
                                    href="#", 
                                    id='nav-carte', 
                                    style={
                                        'color': 'white', 
                                        'textDecoration': 'none',
                                        'padding': '10px'
                                    }
                                )
                            ),
                            html.Li(
                                html.A(
                                    "Histogramme", 
                                    href="#", 
                                    id='nav-histogramme', 
                                    style={
                                        'color': 'white', 
                                        'textDecoration': 'none',
                                        'padding': '10px'
                                    }
                                )
                            ),
                            html.Li(
                              html.A(
                                "Carte de chaleur",
                                href="#",
                                id='nav-carteheat',
                                style={
                                  'color': 'white',
                                  'textDecoration': 'none',
                                  'padding': '10px'
                                }
                              )
                            ),
                            html.Li(
                              html.A(
                                "Diagramme circulaire",
                                href="#",
                                id='nav-circle',
                                style={
                                  'color': 'white',
                                  'textDecoration': 'none',
                                  'padding': '10px'
                                }
                              )
                            )
                        ],
                        style={
                            'listStyleType': 'none',  
                            'padding': '0',  
                            'margin': '0',  
                            'display': 'flex', 
                            'flexDirection': 'column',  #affiche les éléments verticalement
                            'gap': '15px'  #espacement entre les liens
                        }
                    ),

                   
                    

                ]
            )
        ],
        style={'position': 'relative'}
    )
