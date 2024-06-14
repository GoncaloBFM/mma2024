from dash import html, dcc, dash_table
import pandas as pd

def create_dataset_selection():
    options = [
        {'label': 'Human Resources dataset', 'value': 'Human_Resources.csv'},
        {'label': 'House Prices', 'value': 'Housing'},
        {'label': 'Campus Recroutment', 'value': 'Placement_Data_Full_Class.csv'}
    ]


    return html.Div([
        dcc.Dropdown(
            id='dataset-dropdown',
            options=options,
            placeholder='Select a dataset'
        ),
        html.Div(id='dataset-table', style={'overflowX': 'auto'})
    ])

def create_table(data):
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in data.columns],
        data=data.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    )