from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import ohls_chart, help_popup, chart
import dash_bootstrap_components as dbc
import pandas as pd
import src.callbacks.combined_callback  # Import the combined callback
from src.widgets import dataset_selection, input

# Sample data, replace with your actual data source
chart_data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Open': [30, 31, 32, 33, 30, 28, 29, 30, 31, 33, 34, 32, 31, 33, 35, 36, 37, 38, 39, 40, 39, 38, 37, 35, 34, 33, 32, 31, 30, 28],
    'High': [31, 32, 33, 34, 32, 29, 30, 32, 33, 35, 36, 34, 33, 35, 37, 38, 39, 40, 41, 42, 41, 40, 39, 37, 36, 35, 34, 33, 32, 30],
    'Low': [29, 30, 31, 32, 29, 27, 28, 29, 30, 32, 33, 31, 30, 32, 34, 35, 36, 37, 38, 39, 38, 37, 36, 34, 33, 32, 31, 30, 29, 27],
    'Close': [30, 31, 32, 31, 29, 28, 29, 31, 32, 34, 33, 32, 32, 34, 36, 37, 38, 39, 40, 39, 38, 37, 35, 36, 34, 33, 32, 31, 29, 28]
})

code = '''import matplotlib.pyplot as plt

# Example data for the pie chart
labels = ['Rent', 'Groceries', 'Utilities']
sizes = [1200, 300, 150]
colors = ['#ff9999','#66b3ff','#99ff99']
explode = (0.1, 0, 0)  # explode 1st slice (i.e. 'Rent')

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=140)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

plt.title("January Expenses")
plt.show()
'''

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

    initial_chart = chart.create_chart(code, 'Housing')  # Provide the dataset name
    help_popup_widget = help_popup.create_help_popup()
    ohls_chart_widget = ohls_chart.create_ohlc_chart(chart_data)

    tabs = dcc.Tabs([
        dcc.Tab(label='Dataset Selection', children=[
            dataset_selection.create_dataset_selection()
        ]),
        dcc.Tab(label='Prompt & Code', children=[
            input.create_input(),
        ]),
        dcc.Tab(label='Chart/ Visualization', children=[
            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Div(id='old-chart-div', children=[initial_chart], style={'height': '500px', 'overflow': 'auto'}), width=6),
                    dbc.Col(html.Div(id='new-chart-div', children=[], style={'height': '500px', 'overflow': 'auto'}), width=6)
                ])
            ], fluid=True)
        ]),
        dcc.Tab(label='Uncertainty Chart', children=[
            html.Div(ohls_chart_widget, style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%'})
        ]),
    ], style={'marginBottom': '20px'})

    app.layout = dbc.Container([
        help_popup_widget,
        tabs,
    ], fluid=True, id='container')

    app.run_server(debug=True, use_reloader=False)

def main():
    if not Dataset.files_exist():
        print('File', config.AUGMENTED_DATASET_PATH, 'missing or file', config.ATTRIBUTE_DATA_PATH, 'missing or directory', config.IMAGES_DIR, 'missing')
        print('Creating dataset.')
        Dataset.download()

    Dataset.load()

    if len(Dataset.get()) != config.DATASET_SAMPLE_SIZE:
        print('Sample size changed in the configuration. Recalculating features.')
        Dataset.download()
        Dataset.load()

    print('Starting Dash')
    run_ui()

if __name__ == '__main__':
    main()
