from dash import callback, Output, Input

from src.widgets import scatterplot


@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    Input(component_id='projection-radio-buttons', component_property='value'),
    prevent_initial_call=True,
)
def projection_radio_is_clicked(radio_button_value):
    print('radio_button_is_clicked')
    return scatterplot.create_scatterplot_figure(radio_button_value)
