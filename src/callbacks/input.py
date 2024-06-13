from dash import callback, Output, Input, State
from cleanlab_studio import Studio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment variables
api_key = os.getenv('TLM_API_KEY')

# Initialize the language model with your API key
studio = Studio(api_key)
tlm = studio.TLM()

@callback(
    Output('answer-input', 'value'),
    Input('save-button', 'n_clicks'),
    State('prompt-input', 'value'),
    prevent_initial_call=True
)
def save_prompt(n_clicks, prompt):
    if n_clicks > 0 and prompt:
        # Send the prompt to the language model
        response = tlm.prompt(prompt)
        return response["response"]
    return ""
