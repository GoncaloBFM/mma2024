import logging
from dash import callback, html, Output, Input, State, no_update, dcc, ctx
from dash.dependencies import ALL
import pandas as pd
from src.widgets import chart, dataset_selection
from openai import OpenAI
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import io
import base64
import ast

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize clients
USE_OPEN_AI = os.getenv("USE_OPEN_AI", "false").lower() == "true"
CALCULATE_SCORES = os.getenv("CALCULATE_SCORES", "false").lower() == "true"
openai_client = None
tlm_client = None

# Initialize OpenAI client if needed
if USE_OPEN_AI:
    openai_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Initialize TLM client if needed
if not USE_OPEN_AI or CALCULATE_SCORES:
    studio = Studio(api_key=os.environ.get("TLM_API_KEY"))
    tlm_client = studio.TLM()

# Function to get dataset path
def get_dataset_path(dataset_name):
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
    return os.path.join(base_path, f'{dataset_name}.csv')

# Function to load dataset
def load_dataset(dataset_name):
    data_path = get_dataset_path(dataset_name)
    if os.path.exists(data_path):
        return pd.read_csv(data_path)
    raise Exception(f"Dataset {dataset_name} not found")

# Function to send prompt to OpenAI or TLM
def send_prompt(client, prompt, max_tokens):
    if USE_OPEN_AI:
        logger.info(f"Sending prompt to OpenAI: {prompt}")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    else:
        logger.info(f"Sending prompt to TLM: {prompt}")
        return client.prompt(prompt)["response"]

# Function to get code and suggestions
def get_code_and_suggestions(prompt, df, dataset_name):
    try:
        code_prompt = (
            f"Dataset: {dataset_name}\n\nContext: {df.head(2).to_string(index=False)}\n\nPrompt: "
            "You are an AI that strictly conforms to responses in Python code. "
            "Your responses consist of valid python syntax, with no other comments, explanations, reasoning, or dialogue not consisting of valid python. "
            "If you have any comments or remarks they will have a # in front of it. It has to be strict python code. "
            "Use the dataset name, column names, and dataset itself as context for the correct visualization. The code implementation should make use of the correct variable names. "
            "The dataset is already loaded as df. "
            f"{prompt}"
            "Provide only Python code, do not give any reaction other than the code itself, no yapping, no certainly, no nothing like strings, only the code. "
        )

        # Get the code for the original prompt
        code = send_prompt(openai_client if USE_OPEN_AI else tlm_client, code_prompt, 150)
        logger.info(f"Code received: {code}")

        # Get the trustworthiness score for the original prompt
        trustworthiness_score = ""
        if CALCULATE_SCORES:
            trustworthiness_score = tlm_client.prompt(prompt)["trustworthiness_score"]
        logger.info(f"Trustworthiness score: {trustworthiness_score}")

        # Get the suggestions
        improvement_prompt = (
            "An LLM will be provided with the following prompt and a dataset. "
            "Your goal is to improve the prompt so that the LLM returns a more accurate response. "
            "Provide 3 different suggestions how to improve the prompt keeping the same information. "
            "You should return only 1 line containing an array of suggestions and nothing else. "
            "Example response: ['Plot a bar chart', 'Generate a pie chart', 'Plot a visualization'] "
            f"Prompt: {prompt}"
        )
        suggestions_response = send_prompt(openai_client if USE_OPEN_AI else tlm_client, improvement_prompt, 100)
        suggestions_array = ast.literal_eval(suggestions_response)

        # Get the code and trustworthiness score for each suggestion
        suggestions = []
        for suggestion in suggestions_array:
            suggestion_code_prompt = code_prompt.replace(prompt, suggestion)
            suggestion_code = send_prompt(openai_client if USE_OPEN_AI else tlm_client, suggestion_code_prompt, 150)
            suggestion_trustworthiness_score = ""
            if CALCULATE_SCORES:
                suggestion_trustworthiness_score = tlm_client.prompt(suggestion)["trustworthiness_score"]
            suggestions.append((suggestion, suggestion_trustworthiness_score, suggestion_code))
            logger.info(f"Suggestion code received: {suggestion_code}")

        return code, trustworthiness_score, suggestions

    except Exception as e:
        logger.exception(f"Error getting suggestions: {e}")
        return "", "", []

# Function to create suggestion buttons
def create_suggestion_buttons(suggestions):
    return [
        html.Div([
            html.Span(f"({suggestion_score}) ", style={'fontWeight': 'bold'}),
            html.Button(suggestion, id={'type': 'suggestion-button', 'index': i}, n_clicks=0, style={'margin': '5px', 'width': 'auto'}),
            html.Div(suggestion_code, id={'type': 'suggestion-code', 'index': i}, style={'display': 'none'})
        ]) for i, (suggestion, suggestion_score, suggestion_code) in enumerate(suggestions)
    ]

# Callback to update the dataset table based on selected dataset
@callback(
    [Output('dataset-table', 'children'),
     Output('selected-dataset-store', 'data')],
    Input('dataset-dropdown', 'value'),
    prevent_initial_call=True
)
def table_selected(selected_dataset):
    logger.info(f"Updating table for dataset: {selected_dataset}")
    if selected_dataset:
        data = load_dataset(selected_dataset)
        logger.info(f"Dataset {selected_dataset} loaded successfully")
        return dataset_selection.create_table(data), selected_dataset
    return "", ""

# Callback for saving clicked
@callback(
    [Output('answer-input', 'value', allow_duplicate=True),
     Output('suggestions-container', 'children')],
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def save_clicked(n_clicks, prompt, selected_dataset_store):
    logger.info(f"Handling save and suggestions for prompt: {prompt}, n_clicks: {n_clicks}, selected_dataset_store: {selected_dataset_store}")
    if n_clicks > 0 and prompt and selected_dataset_store:
        df = load_dataset(selected_dataset_store)
        
        code, trustworthiness_score, suggestions = get_code_and_suggestions(prompt, df, selected_dataset_store)
        suggestions_list = create_suggestion_buttons(suggestions)
        return code, suggestions_list
    return "", ""

# Callback for submitting clicked
@callback(
    [Output('old-chart-div', 'children'),
     Output('new-chart-div', 'children')],
    Input('submit-button', 'n_clicks'),
    State('answer-input', 'value'),
    State('new-chart-div', 'children'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def submit_clicked(n_clicks, answer_code, current_new_chart, selected_dataset):
    logger.info(f"Submit button clicked. Code that will be executed: {answer_code}, n_clicks: {n_clicks}, selected_dataset: {selected_dataset}")
    if n_clicks > 0 and answer_code and selected_dataset:
        df = load_dataset(selected_dataset)
        try:
            modified_code = answer_code.replace("housing", "df") # ToDo: Do we need that?
            exec(modified_code, {'df': df, 'plt': plt})
            
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            image_base64 = base64.b64encode(buf.read()).decode('utf-8')
            plt.close()
            
            logger.info("Chart updated successfully")

            return current_new_chart, [html.Img(src=f'data:image/png;base64,{image_base64}')]
        
        except Exception as e:
            logger.exception(f"Error while plotting the chart: {e}")
            return no_update, [f"An error occurred while plotting the chart: {str(e)}"]
    return no_update, no_update

@callback(
    [Output('prompt-input', 'value'),
     Output('answer-input', 'value', allow_duplicate=True)],
    Input({'type': 'suggestion-button', 'index': ALL}, 'n_clicks'),
    State({'type': 'suggestion-button', 'index': ALL}, 'children'),
    State({'type': 'suggestion-code', 'index': ALL}, 'children'),
    prevent_initial_call=True
)
def suggestion_clicked(n_clicks, suggestions, suggestion_codes):
    
    # If no suggestion was clicked yet
    if not any(n_clicks):
        return no_update, no_update

    # Identify which button was clicked
    triggered_index = ctx.triggered_id['index']
    logger.info(f"Updating prompt from suggestion index: {triggered_index}")

    return suggestions[triggered_index], suggestion_codes[triggered_index]

@callback(
    [Output('combined-history', 'children'),
     Output('initial-chart-store', 'data'),
     Output('full-history-store', 'data'),
     Output('deleted-history-store', 'data'),
     Output('ohls-chart', 'children')],
    [Input('submit-button', 'n_clicks'),
     Input({'type': 'delete-button', 'index': ALL}, 'n_clicks'),
     Input('clear-history-button', 'n_clicks'),
     Input('restore-history-button', 'n_clicks')],
    [State('prompt-input', 'value'),
     State('selected-dataset-store', 'data'),
     State('answer-input', 'value'),
     State('combined-history', 'children'),
     State('initial-chart-store', 'data'),
     State('full-history-store', 'data'),
     State('deleted-history-store', 'data')],
    prevent_initial_call=True
)
def manage_history(submit_n_clicks, delete_n_clicks, clear_n_clicks, restore_n_clicks,
                   prompt_value, selected_dataset_store, answer_input_value, history_children, initial_chart_present, full_history, deleted_history):
    
    if not ctx.triggered:
        return no_update, no_update, no_update, no_update, no_update

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

    new_combined_history = history_children
    new_initial_chart_store = initial_chart_present
    new_full_history = full_history
    new_deleted_history = deleted_history
    new_ohlc_chart = no_update

    # Handle submit button
    if triggered_id == 'submit-button' and submit_n_clicks > 0 and answer_input_value and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            try:
                modified_code = answer_input_value.replace("housing", "df")
                exec(modified_code, {'df': data, 'plt': plt, 'pd': pd})

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close()

                new_prompt_div = html.Div([html.P(prompt_value, style={'text-align': 'center'})], style={'flex': '1', 'padding': '10px'})
                new_chart_div = html.Div([html.Img(src=f'data:image/png;base64,{image_base64}')], style={'flex': '1', 'padding': '10px'})
                delete_button = html.Button('Delete', id={'type': 'delete-button', 'index': len(full_history)}, n_clicks=0)

                new_entry = html.Div([new_prompt_div, new_chart_div, delete_button], style={'display': 'flex', 'justify-content': 'space-between', 'align-items': 'center'})

                if initial_chart_present:
                    new_combined_history = [new_entry]
                    new_full_history = [new_entry]
                    new_initial_chart_store = False  # Set the flag to False after removing the initial entry
                else:
                    new_combined_history = [new_entry] + history_children
                    new_full_history = [new_entry] + full_history
            except Exception as e:
                return no_update, no_update, no_update, no_update, [html.Div(f"An error occurred while plotting the chart: {str(e)}")] + history_children
        else:
            return no_update, no_update, no_update, no_update, [html.Div(f"Dataset {selected_dataset_store} not found.")] + history_children

    # Handle delete button
    if 'delete-button' in triggered_id:
        index = int(triggered_id.split(':')[1].split(',')[0])
        deleted_entry = new_combined_history.pop(len(new_combined_history) - 1 - index)
        new_deleted_history.append(deleted_entry)
        if initial_chart_present and not new_combined_history:
            new_initial_chart_store = True

    # Handle clear history button
    if triggered_id == 'clear-history-button' and clear_n_clicks > 0:
        new_combined_history = []
        new_deleted_history = history_children

    # Handle restore history button
    if triggered_id == 'restore-history-button' and restore_n_clicks > 0:
        if not full_history:
            new_combined_history = new_deleted_history
        else:
            new_combined_history = new_full_history + new_deleted_history
        new_deleted_history = []

    return new_combined_history, new_initial_chart_store, new_full_history, new_deleted_history, new_ohlc_chart
