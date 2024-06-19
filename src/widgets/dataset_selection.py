from dash import html, dcc, dash_table

def create_dataset_selection():
    options = [
        {'label': 'Human Resources dataset', 'value': 'Human_Resources'},
        {'label': 'House Prices', 'value': 'Housing'},
        {'label': 'Campus Recruitment', 'value': 'Placement_Data_Full_Class'},
        {'label': 'Supermarket Sales', 'value': 'supermarket_sales'},
        {'label': 'Hotel Bookings', 'value': 'hotel_booking'}
    ]

    return html.Div([
        dcc.Dropdown(
            id='dataset-dropdown',
            options=options,
            placeholder='Select a dataset'
        ),
        html.Div(id='dataset-table', style={'overflowX': 'auto'}),
        dcc.Store(id='selected-dataset-store')
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
