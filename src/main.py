from dash import Dash, html, dcc
from src import config
from src.Dataset import Dataset
from src.widgets import projection_radio_buttons, gallery, scatterplot, wordcloud, graph, heatmap,histogram
from src.widgets.table import create_table
import dash_bootstrap_components as dbc

import callbacks.table
import callbacks.scatterplot
import callbacks.projection_radio_buttons
import callbacks.heatmap
import callbacks.wordcloud
import callbacks.histogram
import callbacks.gallery
import callbacks.deselect_button
import callbacks.help_button
import callbacks.graph

def run_ui():
    external_stylesheets = [dbc.themes.BOOTSTRAP]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    help_popup_widget = help_popup.create_help_popup()
    projection_radio_buttons_widget = projection_radio_buttons.create_projection_radio_buttons()
    table_widget = create_table()
    scatterplot_widget = scatterplot.create_scatterplot(config.DEFAULT_PROJECTION)
    wordcloud_widget = wordcloud.create_wordcloud()
    gallery_widget = gallery.create_gallery()
    graph_widget = graph.create_graph()
    heatmap_widget = heatmap.create_heatmap()
    histogram_widget = histogram.create_histogram()

    right_tab = dcc.Tabs([
        dcc.Tab(label='wordcloud', children=wordcloud_widget),
        dcc.Tab(label='sample images', children=gallery_widget),
        dcc.Tab(label='histogram', children=histogram_widget),
        dcc.Tab(label='graph', children=graph_widget),
        dcc.Tab(label='heatmap', children=[heatmap_widget])
    ])

    app.layout = dbc.Container([
        help_popup_widget,
        dbc.Stack([
            projection_radio_buttons_widget,
            dbc.Button('Deselect everything', id='deselect-button', class_name="btn btn-outline-primary ms-auto header-button"),
            dbc.Button('Help', id='help-button', class_name="btn btn-outline-primary header-button")
        ], id='header', direction="horizontal"),
        dbc.Row([
            dbc.Col(scatterplot_widget, width=6, className='main-col'),
            dbc.Col(right_tab, width=6, className='main-col')],
            className='top-row', justify='between'),
        dbc.Row([
            dbc.Col(table_widget, className='main-col')
        ], className='bottom-row')
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