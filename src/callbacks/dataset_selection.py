from dash import callback, Output, Input
import pandas as pd
from src.widgets.dataset_selection import create_table
import os

@callback(
    [Output('dataset-table', 'children'),
     Output('selected-dataset-store', 'data')],
    Input('dataset-dropdown', 'value')
)
def update_table(selected_dataset):
    if selected_dataset:
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../dataset/ourdata'))
        data_path = os.path.join(base_path, f'{selected_dataset}.csv')
        data = pd.read_csv(data_path)
        return create_table(data), selected_dataset
    return "", ""
