from dash import callback, Output, Input, State
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('TLM_API_KEY')

# Initialize the language model with your API key
studio = Studio(api_key)
tlm = studio.TLM()

@callback(
    [Output('answer-input', 'value'),
     Output('selected-dataset-store', 'data')],
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    State('selected-dataset-store', 'data'),
    prevent_initial_call=True
)
def save_prompt(n_clicks, prompt, selected_dataset):
    if n_clicks > 0 and prompt:
        # Extract column names to help the LLM understand the dataset structure
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
        data_path = os.path.join(base_path, f'{selected_dataset}.csv')
        df = pd.read_csv(data_path)
        column_names = ", ".join(df.columns)

        # Modify the prompt to include the column names and dataset name
        modified_prompt = f"Dataset: {selected_dataset}\n\nDataset columns: {column_names}\n\nPrompt: {prompt}"
        response = tlm.prompt(modified_prompt)
        return response["response"], selected_dataset
    return "", selected_dataset
