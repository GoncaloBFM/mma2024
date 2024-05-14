import dash_ag_grid
from dash import dcc
import dash_bootstrap_components as dbc

from src.Dataset import Dataset


def create_table():
    return dbc.Stack([
        create_table_filter(),
        create_table_grid()
    ],
        className='stretchy-widget',
        id='table'
    )


def create_table_filter():
    return dcc.Input(id="table-filter", placeholder="filter table...")


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
            "rowMultiSelectWithClick": True,
        },
        className='stretchy-widget ag-theme-alpine',
        style={'width': '', 'height': ''},
        id='grid'
    )
