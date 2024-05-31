from dash import Input, Output, callback, State

@callback(
    Output("grid", "selectedRows"),
    Input("wordcloud", "click"),
    prevent_initial_call=True,
)
def wordcloud_is_clicked(wordcloud_selection):
    print('Wordcloud is clicked')
    class_name = wordcloud_selection[0]
    print(class_name)
    return {'function': f'params.data.class_name == "{class_name}"'}
