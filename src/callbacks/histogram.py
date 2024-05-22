# from dash import Input, Output, callback, State

# @callback(
#     Output("grid", "selectedRows"),
#     State('scatterplot', 'figure'),
#     Input("histogram", "click"),
#     prevent_initial_call=True,
# )
# def histogram_is_clicked(scatterplot_fig, histogram_selection):
#     print('Wordcloud is clicked')
#     class_name = histogram_selection[0]
#     print(class_name)
#     return {'function': f'params.data.class_name == "{class_name}"'}
