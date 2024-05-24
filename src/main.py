from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import projection_radio_buttons, gallery, scatterplot, wordcloud, placeholder, graph, heatmap,histogram
from src.widgets.table import create_table
import dash_bootstrap_components as dbc

import callbacks.table
import callbacks.scatterplot
import callbacks.projection_radio_buttons
import callbacks.heatmap
import callbacks.wordcloud
# import callbacks.histogram

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons_widget = projection_radio_buttons.create_projection_radio_buttons()
    table_widget = create_table()
    scatterplot_widget = scatterplot.create_scatterplot(config.DEFAULT_PROJECTION)
    wordcloud_widget = wordcloud.create_wordcloud()
    gallery_widget = gallery.create_gallery()
    # placeholder_widget = placeholder.create_placeholder()
    graph_widget = graph.create_graph()
    heatmap_widget = heatmap.create_heatmap()
    histogram_widget= histogram.create_histogram()

    left_tab = dcc.Tabs([
        dcc.Tab(label='table', children=table_widget),
        # dcc.Tab(label='placeholder', children=placeholder_widget)
        dcc.Tab(label='histogram', children=histogram_widget)
    ])

    right_tab = dcc.Tabs([
        dcc.Tab(label='sample images', children=gallery_widget),
        dcc.Tab(label='graph', children=graph_widget), 
        dcc.Tab(label='heatmap', children=[heatmap_widget])
    ])

    app.layout = dbc.Container([
        html.Div(
            projection_radio_buttons_widget,
            id='header'
        ),
        dbc.Row([
            dbc.Col(scatterplot_widget, width=True, className='main-col'),
            dbc.Col(wordcloud_widget, width='auto', align="center")],
            className='g-10 main-row', justify='between'),
        dbc.Row([
            dbc.Col(left_tab, className='main-col', width=6),
            dbc.Col(right_tab, className='main-col', width=6)
        ], className='g-10 main-row')
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