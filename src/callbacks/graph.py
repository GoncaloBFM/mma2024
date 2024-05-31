from dash import Input, Output, callback, State

@callback(
    Output("grid", "selectedRows", allow_duplicate=True),
    Input("graph", "clickData"),
    prevent_initial_call=True,
)
def graph_is_clicked(clickData):
    print('Graph is clicked')
    
    if clickData is None or 'points' not in clickData or len(clickData['points']) == 0:
        return {'function': 'params.data.class_name == ""'}

    class_name = clickData['points'][0]['text']  # Extract the node's text which holds the class_name
    print(class_name)
    return {'function': f'params.data.class_name == "{class_name}"'}

