from dash import Input, Output

def register_menu_callbacks(app):
    @app.callback(
    Output('side-menu', 'style'),
    Input('menu-icon', 'n_clicks'),
    prevent_initial_call=True
    )
    def toggle_menu(n_clicks):
        if n_clicks % 2 == 1:
            return {
                'position': 'fixed',
                'top': '15',
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
        else:
            return {
                'position': 'fixed',
                'top': '0',
                'left': '-1000px',
                'width': '250px',
                'height': '100%',
                'backgroundColor': '#333',
                'color': 'white',
                'padding': '0px',
                'boxShadow': '2px 0px 5px rgba(0,0,0,0.5)',
                'transition': 'left 0.3s ease',
                'zIndex': '999'
            }

