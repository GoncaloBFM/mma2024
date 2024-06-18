from dash import callback, Output, Input, State, no_update
import pandas as pd
from src.widgets import chart, dataset_selection
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv
import dash

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('TLM_API_KEY')

# Initialize the language model with your API key
studio = Studio(api_key)
tlm = studio.TLM()

# Function to get dataset path
def get_dataset_path(dataset_name):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
    return os.path.join(base_path, f'{dataset_name}.csv')

@callback(
    [Output('dataset-table', 'children'),
     Output('selected-dataset-store', 'data'),
     Output('answer-input', 'value')],
    [Input('dataset-dropdown', 'value'),
     Input('save-button', 'n_clicks')],
    [State('prompt-input', 'value'),
     State('selected-dataset-store', 'data')],
    prevent_initial_call=True
)
def update_table_and_save_prompt(selected_dataset, n_clicks, prompt, selected_dataset_store):
    ctx = dash.callback_context

    if not ctx.triggered:
        return "", "", ""
    
    trigger_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if trigger_id == 'dataset-dropdown' and selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            return dataset_selection.create_table(data), selected_dataset, no_update
        else:
            return f"Dataset {selected_dataset} not found.", "", no_update

    if trigger_id == 'save-button' and n_clicks > 0 and prompt:
        if selected_dataset_store:
            data_path = get_dataset_path(selected_dataset_store)
            if os.path.exists(data_path):
                df = pd.read_csv(data_path)
                column_names = ", ".join(df.columns)
                modified_prompt = f"Dataset: {selected_dataset_store}\n\nDataset columns: {column_names}\n\nPrompt: {prompt}"
                response = tlm.prompt(modified_prompt)
                return no_update, selected_dataset_store, response["response"]
            else:
                return no_update, selected_dataset_store, f"Dataset {selected_dataset_store} not found."
    
    return no_update, no_update, no_update

@callback(
    [Output('old-chart-div', 'children'),
     Output('new-chart-div', 'children')],
    Input('submit-button', 'n_clicks'),
    State('answer-input', 'value'),
    State('new-chart-div', 'children'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def update_chart(n_clicks, answer_code, current_new_chart, selected_dataset):
    if n_clicks > 0 and answer_code and selected_dataset:
        try:
            data_path = get_dataset_path(selected_dataset)
            if os.path.exists(data_path):
                data = pd.read_csv(data_path)
                new_chart = chart.create_chart(answer_code, data)
                return current_new_chart, [new_chart]
            else:
                return no_update, [f"Dataset {selected_dataset} not found."]
        except Exception as e:
            return no_update, [f"An error occurred while plotting the chart: {str(e)}"]
    return no_update, no_update
