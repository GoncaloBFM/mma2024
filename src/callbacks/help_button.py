from dash import Output, callback, Input


@callback(
    Output("help-popup", "is_open"),
    Input("help-button", "n_clicks"),
    prevent_initial_call=True,
)
def help_button_is_pressed(_):
    return True
