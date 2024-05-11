from dash import callback, Output, Input

from src.widgets import scatterplot


@callback(
    Output('table', 'style', allow_duplicate=True),
    Output('placeholder', 'style', allow_duplicate=True),
    Input(component_id='left-tab-radio-buttons', component_property='value'),
    prevent_initial_call=True,
)
def left_tab_radio_is_clicked(radio_button_value):
    if radio_button_value == 'table':
        return {'display':''},{'display':'none'}
    elif radio_button_value == 'placeholder':
        return {'display': 'none'},{'display': ''}

    raise Exception('Unknown value for left tab radio button:', radio_button_value)
