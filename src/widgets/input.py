from dash import dcc, html

def create_input():
    return html.Div(
        style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'width': '100%'},
        children=[
            html.Div(
                style={'width': '80%', 'marginBottom': '20px'},
                children=[
                    html.Label('Prompt:'),
                    dcc.Textarea(
                        id='prompt-input',
                        style={'width': '100%', 'height': '200px'},  # Adjusted height for larger input area
                        placeholder='Enter the prompt here...'
                    ),
                ]
            ),
            html.Div(
                style={'width': '80%', 'marginBottom': '20px'},
                children=[
                    html.Label('Answer:'),
                    dcc.Textarea(
                        id='answer-input',
                        style={'width': '100%', 'height': '100px'},
                        placeholder='Enter the answer here...'
                    ),
                ]
            ),
            html.Button('Submit', id='submit-button', n_clicks=0)
        ]
    )
