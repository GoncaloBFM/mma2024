from dash import Input, Output, callback, State
import plotly.graph_objects as go

from src.widgets import scatterplot


@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    Output('grid', 'deselectAll', allow_duplicate=True),
    State('projection-radio-buttons', 'value'),
    State('scatterplot', 'figure'),
    Input('deselect-button', 'n_clicks'),
    prevent_initial_call=True,
)
def deselect_button_is_pressed(projection_selected, scatterplot_fig, _):
    print('Deselect button is clicked')
    new_scatterplot_fig = scatterplot.create_scatterplot_figure(projection_selected)
    new_scatterplot_fig['layout'] = scatterplot_fig['layout']
    new_scatterplot_fig['layout']['selections'] = None
    return new_scatterplot_fig, True
