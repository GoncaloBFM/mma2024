from dash import callback, Output, Input, State, no_update
from src.widgets import chart

@callback(
    [Output('old-chart-div', 'children'),
     Output('new-chart-div', 'children')],
    Input('submit-button', 'n_clicks'),
    State('answer-input', 'value'),
    State('new-chart-div', 'children'),
    prevent_initial_call=True
)
def update_chart(n_clicks, answer_code, current_new_chart):
    if n_clicks > 0 and answer_code:
        try:
            new_chart = chart.create_chart(answer_code)
            # Move the current new chart to old chart and display the new valid chart
            return current_new_chart, [new_chart]
        except Exception as e:
            # Display the error on the right and keep the old chart unchanged
            return no_update, [f"An error occurred while plotting the chart: {str(e)}"]
    return no_update, no_update
