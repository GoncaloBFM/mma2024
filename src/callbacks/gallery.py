import dash
from dash import callback, Output, Input, MATCH, State, ALL, no_update
from dash.exceptions import PreventUpdate


@callback(
    Output("grid", "selectedRows", allow_duplicate=True),
    Input({'type': 'gallery-card', 'index': ALL}, 'n_clicks'),
    prevent_initial_call=True,
)
def gallery_image_is_clicked(n_clicks):
    if all(e is None for e in n_clicks):
        return no_update

    print('Gallery is clicked')
    class_name = dash.callback_context.triggered_id['index']
    return {'function': f'params.data.class_name == "{class_name}"'}
