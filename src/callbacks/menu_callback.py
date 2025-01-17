from dash import Input, Output, dash

def register_menu_callbacks(app: dash.Dash):
    """
    Enregistre un callback pour gérer l'ouverture et la fermeture du menu latéral

    Args:
        app (dash.Dash): L'application Dash
    """
    @app.callback(
        Output('side-menu', 'style'),
        Input('menu-icon', 'n_clicks'),
        prevent_initial_call=True
    )
    def toggle_menu(n_clicks: int) -> dict:
        """
        Gère le style du menu latéral en fonction du nombre de clics sur l'icône du menu

        Args:
            n_clicks (int): Nombre de clics sur l'icône du menu

        Returns:
            dict: Style CSS appliqué au menu latéral
        """
        #vérifie si aucun clic n'a été effectué
        if n_clicks is None or n_clicks % 2 == 0:
            return {
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
            }
        else:
            return {
                'position': 'fixed',
                'top': '0',
                'left': '0',  
                'width': '250px',
                'height': '100%',
                'backgroundColor': '#333',
                'color': 'white',
                'padding': '15px',
                'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
                'transition': 'left 0.3s ease',
                'zIndex': '999'
            }
