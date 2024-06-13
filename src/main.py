from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import ohls_chart, projection_radio_buttons, gallery, scatterplot, wordcloud, graph, heatmap, histogram, help_popup, input, chart
from src.widgets.table import create_table
import dash_bootstrap_components as dbc
import pandas as pd

import callbacks.chart
import callbacks.input

# Sample data, replace with your actual data source
chart_data = pd.DataFrame({
    'Date': pd.date_range(start='2023-01-01', periods=30, freq='D'),
    'Open': [30, 31, 32, 33, 30, 28, 29, 30, 31, 33, 34, 32, 31, 33, 35, 36, 37, 38, 39, 40, 39, 38, 37, 35, 34, 33, 32, 31, 30, 28],
    'High': [31, 32, 33, 34, 32, 29, 30, 32, 33, 35, 36, 34, 33, 35, 37, 38, 39, 40, 41, 42, 41, 40, 39, 37, 36, 35, 34, 33, 32, 30],
    'Low': [29, 30, 31, 32, 29, 27, 28, 29, 30, 32, 33, 31, 30, 32, 34, 35, 36, 37, 38, 39, 38, 37, 36, 34, 33, 32, 31, 30, 29, 27],
    'Close': [30, 31, 32, 31, 29, 28, 29, 31, 32, 34, 33, 32, 32, 34, 36, 37, 38, 39, 40, 39, 38, 37, 35, 36, 34, 33, 32, 31, 29, 28]
})

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    input_widget = input.create_input()
    help_popup_widget = help_popup.create_help_popup()
    projection_radio_buttons_widget = projection_radio_buttons.create_projection_radio_buttons()
    # table_widget = create_table()
    # scatterplot_widget = scatterplot.create_scatterplot(config.DEFAULT_PROJECTION)
    # wordcloud_widget = wordcloud.create_wordcloud()
    # gallery_widget = gallery.create_gallery()
    # graph_widget = graph.create_graph()
    # heatmap_widget = heatmap.create_heatmap()
    # histogram_widget = histogram.create_histogram()
    ohls_chart_widget = ohls_chart.create_ohlc_chart(chart_data)

    right_tab = dcc.Tabs([
        dcc.Tab(label='chart', children=[html.Div(id='chart-div', style={'display': 'flex', 'justify-content': 'center', 'align-items': 'center', 'height': '100%'})]),
        # dcc.Tab(label='wordcloud', children=wordcloud_widget),
        # dcc.Tab(label='sample images', children=gallery_widget),
        # dcc.Tab(label='histogram', children=histogram_widget),
        # dcc.Tab(label='graph', children=graph_widget),
        # dcc.Tab(label='heatmap', children=[heatmap_widget]),
        dcc.Tab(label='ohlc chart', children=[ohls_chart_widget]),
    ])

    app.layout = dbc.Container([
        help_popup_widget,
        dbc.Stack([
            projection_radio_buttons_widget,
            dbc.Button('Deselect everything', id='deselect-button', class_name="btn btn-outline-primary ms-auto header-button"),
            dbc.Button('Help', id='help-button', class_name="btn btn-outline-primary header-button")
        ], id='header', direction="horizontal"),
        dbc.Row([
            dbc.Col(input_widget, width=6, class_name='main-col'),
            dbc.Col(right_tab, width=6, class_name='main-col')
        ], className='top-row', justify='between'),
        # dbc.Row([
        #     dbc.Col(scatterplot_widget, width=6, className='main-col'),
        #     dbc.Col(right_tab, width=6, class_name='main-col')],
        #     className='top-row', justify='between'),
        # dbc.Row([
        #     dbc.Col(table_widget, className='main-col')
        # ], className='bottom-row')
    ], fluid=True, id='container')

    app.run(debug=True, use_reloader=False)

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
