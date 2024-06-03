from dash import callback, Output, Input

from src.widgets import scatterplot


@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    Output('grid', 'deselectAll', allow_duplicate=True),
    Input('projection-radio-buttons', 'value'),
    prevent_initial_call=True,
)
def projection_radio_is_clicked(radio_button_value):
    print('Radio button clicked')
    return scatterplot.create_scatterplot_figure(radio_button_value), True
