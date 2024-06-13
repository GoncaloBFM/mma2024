from dash import dcc

def create_dataset_dropdown():
    return dcc.Dropdown(
        id='dataset-dropdown',
        options=[
            {'label': 'Dataset 1', 'value': 'dataset1.csv'},
            {'label': 'Dataset 2', 'value': 'dataset2.csv'},
            {'label': 'Dataset 3', 'value': 'dataset3.csv'},
        ],
        value='dataset1.csv'
    )