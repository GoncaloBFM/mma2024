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

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with your API key
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# # Initialize the TLM client with your API key
# studio = Studio(api_key=os.environ.get("TLM_API_KEY"))
# tlm = studio.TLM()

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
    logger.info(f"Updating table for dataset: {selected_dataset}")
    if selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            logger.info(f"Dataset {selected_dataset} loaded successfully")
            return dataset_selection.create_table(data), selected_dataset
        else:
            logger.warning(f"Dataset {selected_dataset} not found")
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
    logger.info(f"Handling save and suggestions for prompt: {prompt}")
    if n_clicks > 0 and prompt and selected_dataset_store:
        data_path = get_dataset_path(selected_dataset_store)
        if os.path.exists(data_path):
            df = pd.read_csv(data_path)
            logger.info(f"Dataset {selected_dataset_store} loaded successfully for suggestions")
            
            code_prompt = (
                f"Dataset: {selected_dataset_store}\n\nContext: {df.head(2).to_string(index=False)}\n\nPrompt: "
                "You are an AI that strictly conforms to responses in Python code. "
                "Your responses consist of valid python syntax, with no other comments, explanations, reasoning, or dialogue not consisting of valid python. "
                "If you have any comments or remarks they will have a # in front of it. It has to be strict python code. "
                "Use the dataset name, column names, and dataset itself as context for the correct visualization. The code implementation should make use of the correct variable names. "
                "The dataset is already loaded as df. "
                f"{prompt}"
                "Provide only Python code, do not give any reaction other than the code itself, no yapping, no certainly, no nothing like strings, only the code. "
            )

            code_output = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": code_prompt}
                ],
                max_tokens=150
            )
            code = code_output.choices[0].message.content.strip()
            logger.info(f"Code: {code}")

            # # Evaluate the trustworthiness of the prompt
            # trustworthiness_score = tlm.prompt(prompt)["trustworthiness_score"]
            # logger.info(f"Trustworthiness score: {trustworthiness_score}")

            improvement_prompt = (
                "An LLM will be provided with the following prompt and a dataset. "
                "Your goal is to improve the prompt so that the LLM returns a more accurate response. "
                "Provide 3 different suggestions how to improve the prompt keeping the same information. "
                "You should return only 1 line containing an array of suggestions and nothing else. "
                "Example response: ['Plot a bar chart', 'Generate a pie chart', 'Plot a visualization'] "
                f"Prompt: {prompt}"
            )
            try:
                suggestions_output = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": improvement_prompt}
                    ],
                    max_tokens=100
                )
                suggestions_content = suggestions_output.choices[0].message.content.strip()
                suggestions = ast.literal_eval(suggestions_content)
                logger.info(f"Suggestions received: {suggestions}")

                suggestions_list = [
                    # html.Div([
                    #     html.Span(f"({score:.2f}) ", style={'fontWeight': 'bold'}),
                    #     html.Button(suggestion, id={'type': 'suggestion-button', 'index': i}, n_clicks=0, style={'margin': '5px', 'width': 'auto'})
                    # ]) for i, (suggestion, score) in enumerate(zip(suggestions, trustworthiness_score))
                    html.Div([
                        html.Button(suggestion, id={'type': 'suggestion-button', 'index': i}, n_clicks=0, style={'margin': '5px', 'width': 'auto'})
                    ]) for i, suggestion in enumerate(suggestions)
                ]

                return code, suggestions_list
            except Exception as e:
                logger.error(f"Error during suggestions: {e}")
                return code, [f"An error occurred: {e}"]
        else:
            logger.warning(f"Dataset {selected_dataset_store} not found")
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
    logger.info(f"Updating chart with answer code: {answer_code}")
    if n_clicks > 0 and answer_code and selected_dataset:
        data_path = get_dataset_path(selected_dataset)
        if os.path.exists(data_path):
            data = pd.read_csv(data_path)
            logger.info(f"Dataset {selected_dataset} loaded successfully for chart update")
            try:
                modified_code = answer_code.replace("housing", "df")
                exec(modified_code, {'df': data, 'plt': plt})
                
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                image_base64 = base64.b64encode(buf.read()).decode('utf-8')
                plt.close()
                
                logger.info("Chart updated successfully")
                return current_new_chart, [html.Img(src=f'data:image/png;base64,{image_base64}')]
            except Exception as e:
                logger.error(f"Error while plotting the chart: {e}")
                return no_update, [f"An error occurred while plotting the chart: {str(e)}"]
        else:
            logger.warning(f"Dataset {selected_dataset} not found")
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
    if not ctx_triggered or ctx_triggered['type'] != 'suggestion-button':
        return no_update
    triggered_index = ctx_triggered['index']
    logger.info(f"Updating prompt from suggestion index: {triggered_index}")
    return suggestions[triggered_index]
