from dash import callback, Output, Input, State
from src.widgets import chart

@callback(
    Output('chart-div', 'children'),
    Input('submit-button', 'n_clicks'),
    State('answer-input', 'value'),
    prevent_initial_call=True
)
def update_chart(n_clicks, answer_code):
    if n_clicks > 0 and answer_code:
        return chart.create_chart(answer_code)
    return []
