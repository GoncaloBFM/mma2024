from dash import Input, Output, callback, State

@callback(
    Output("grid", "selectedRows", allow_duplicate=True),
    Input("graph", "clickData"),
    prevent_initial_call=True,
)
def graph_is_clicked(click_data):
    print('Graph is clicked')
    
    if click_data is None or 'points' not in click_data or len(click_data['points']) == 0:
        return {'function': 'params.data.class_name == ""'}

    class_name = click_data['points'][0]['text']  # Extract the node's text which holds the class_name
    print(class_name)
    return {'function': f'params.data.class_name == "{class_name}"'}

