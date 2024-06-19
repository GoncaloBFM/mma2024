from dash import callback, html, Output, Input, State, no_update, dcc, ctx
from dash.dependencies import ALL
import pandas as pd
from src.widgets import chart, dataset_selection
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64
import ast

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
     Output('selected-dataset-store', 'data')],
    Input('dataset-dropdown', 'value'),
    prevent_initial_call=True
)
def update_table(selected_dataset):
    if selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            return dataset_selection.create_table(data), selected_dataset
        else:
            return f"Dataset {selected_dataset} not found.", ""
    return "", ""

@callback(
    [Output('answer-input', 'value'),
     Output('suggestions-container', 'children')],
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def handle_save_and_suggestions(n_clicks, prompt, selected_dataset_store):
    if n_clicks > 0 and prompt and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            #give the first 2 rows of the dataset as context
            modified_prompt = f"Dataset: {selected_dataset_store}\n\nContext: {df.head(2).to_string(index=False)}\n\nPrompt: {prompt}"
            response = tlm.prompt(modified_prompt)
            answer_response = response["response"]
            
            improvement_prompt = (
                "An LLM will be provided with the following prompt and a dataset. "
                "Your goal is to improve the prompt so that the LLM returns a more accurate response. "
                "Provide 3 different suggestions how to improve parts of the prompt. "
                "You should return only 1 line containing an array of suggestions and nothing else. "
                "Example response: ['Plot a bar chart', 'Generate a pie chart', 'Plot a visualization'] "
                f"Prompt: {prompt}"
            )
            try:
                suggestions_output = tlm.prompt(improvement_prompt)
                suggestions = ast.literal_eval(suggestions_output["response"])

                improved_outputs = [tlm.prompt(suggestion) for suggestion in suggestions]

                suggestions_list = [
                    html.Div([
                        html.Span(f"({output['trustworthiness_score']:.2f}) ", style={'fontWeight': 'bold'}),
                        html.Button(suggestion, id={'type': 'suggestion-button', 'index': i}, n_clicks=0, style={'margin': '5px', 'width': 'auto'})
                    ]) for i, (suggestion, output) in enumerate(zip(suggestions, improved_outputs))
                ]

                return answer_response, suggestions_list
            except Exception as e:
                return answer_response, [f"An error occurred: {e}"]
        else:
            return "", ""
    return "", ""

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
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            try:
                modified_code = answer_code.replace("housing", "df")
                exec(modified_code, {'df': data, 'plt': plt})
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close()
                
                return current_new_chart, [html.Img(src=f'data:image/png;base64,{image_base64}')]
            except Exception as e:
                return no_update, [f"An error occurred while plotting the chart: {str(e)}"]
        else:
            return no_update, [f"Dataset {selected_dataset} not found."]
    return no_update, no_update

@callback(
    Output('prompt-input', 'value'),
    Input({'type': 'suggestion-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'suggestion-button', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def update_prompt_from_suggestion(n_clicks, suggestions):
    ctx_triggered = ctx.triggered_id
    if not ctx_triggered:
        return no_update
    triggered_index = ctx_triggered['index']
    return suggestions[triggered_index]
