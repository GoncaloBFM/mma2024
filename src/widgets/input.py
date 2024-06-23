from dash import dcc, html
import dash_bootstrap_components as dbc

def create_input():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col(dcc.Textarea(id='prompt-input', style={'width': '100%', 'height': 200}, placeholder='Enter your prompt here...'), width=12),
                    dbc.Col(dcc.Textarea(id='answer-input', style={'width': '100%', 'height': 200}, placeholder='Answer will be displayed here...'), width=12)
                ]),
                dbc.Row([
                    dbc.Col(dbc.Button('Save', id='save-button', color='primary'), width='auto'),
                    dbc.Col(dbc.Button('Submit', id='submit-button', color='success'), width='auto')
                ], justify='center', style={'marginTop': '20px'}),
                dcc.Store(id='score-store'),
            ], width=6),
            dbc.Col([
                html.Div([
                    html.Label('Suggestions:'),
                    html.Div(id='suggestions-container', style={'height': '300px', 'overflowY': 'scroll'}),
                ])
            ], width=6)
        ])
    ], fluid=True)
