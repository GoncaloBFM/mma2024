import dash_ag_grid
from dash import dcc, html

from src.Dataset import Dataset


def create_table():
    return html.Div([
        create_table_grid()
    ],
        className='stretchy-widget',
        id='table'
    )

def create_table_grid():
    return dash_ag_grid.AgGrid(
        columnDefs=[
            {"field": "class_name"},
            {"field": "count_in_selection"},
            {"field": "total_count", }
        ],
        rowData=[],
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "pagination": False,
            "paginationAutoPageSize": True,
            "suppressCellFocus": True,
            "rowSelection": "multiple",
        },
        defaultColDef={"filter": "agTextColumnFilter"},
        className='stretchy-widget ag-theme-alpine',
        style={'width': '', 'height': ''},
        id='grid'
    )
