from dash import Input, Output, callback, State

from src.Dataset import Dataset
from src.widgets import scatterplot


@callback(
    Output("grid", "selectedRows"),
    State('scatterplot', 'figure'),
    Input("wordcloud", "click"),
    prevent_initial_call=True,
)
def wordcloud_is_clicked(scatterplot_fig, wordcloud_selection):
    print('Wordcloud is clicked')
    class_name = wordcloud_selection[0]
    print(class_name)
    return {'function': f'params.data.class_name == "{class_name}"'}
