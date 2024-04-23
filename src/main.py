import base64
import os.path
from io import BytesIO

import pandas
import dash_ag_grid

import plotly.express as px
from wordcloud import WordCloud

from src import definitions
from src.dataloader import cub_loader
from src import feature_engineering
from dash import Dash, html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc

IMAGE_GALLERY_SIZE = 34
IMAGE_GALLERY_ROW_SIZE = 4
WORDCLOUD_IMAGE_HEIGHT = 450
WORDCLOUD_IMAGE_WIDTH = 600

def run_ui():
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons = dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['t-SNE', 'UMAP']],
        value='UMAP',
        inline=True,
        id='projection-radio-buttons'
    )

    table = dash_ag_grid.AgGrid(
        columnDefs=[
            {"field": "class_id"},
            {"field": "class_name"},
            {"field": "count_in_selection"},
            {"field": "total_count"}
            ],
        rowData=[],
        columnSize="sizeToFit",
        dashGridOptions={
            "rowSelection": "single",
            "pagination": True,
            "paginationAutoPageSize": True
        },
        className='ag-theme-alpine widget',
        style={'width': '', 'height': ''},
        id='table'
    )

    scatterplot_figure = radio_button_is_clicked('UMAP')
    scatterplot_figure.update_layout(dragmode='select')
    scatterplot_figure.update_traces(customdata=Dataset.get().index)

    scatterplot = dcc.Graph(
        figure=scatterplot_figure,
        id='scatterplot',
        className='widget',
        config={
            'displaylogo': False,
            'modeBarButtonsToRemove':
                [
                    'zoom',
                    'pan',
                    'zoomIn',
                    'zoomOut',
                    'autoScale',
                    'resetScale'
                ]
        }
    )

    wordcloud_image = html.Img(
        id='wordcloud',
        className='widget border-widget',
    )

    gallery_card = dbc.Card(
        [
            dbc.CardHeader(f'Sample of images from selection'),
            dbc.CardBody([], id='gallery', className='gallery'),
        ],
    className='widget border-widget')

    app.layout = dbc.Container([
        html.Div('Multimedia analytics demo', className='text-primary text-center fs-3 header'),
        dbc.Stack([
            html.Div('Projection: '),
            projection_radio_buttons,
        ], direction="horizontal"),
        dbc.Stack([
            scatterplot,
            table
        ], direction="horizontal"),
        dbc.Stack([
            wordcloud_image,
            gallery_card
        ], direction="horizontal"),
    ])
    app.run(debug=True, use_reloader=False)



@callback(
    Output(component_id='scatterplot', component_property='figure', allow_duplicate=True),
    State('scatterplot', 'figure'),
    Input("table", "selectedRows"),
    prevent_initial_call=True,
)
def table_row_is_clicked(scatterplot, selected_row):
    print('table_row_is_clicked')
    if selected_row:
        selected_class = selected_row[0]['class_id']
        colors = Dataset.get()['class_id'].map(lambda x: 'red' if selected_class == x else 'blue')
    else:
        colors = 'blue'

    scatterplot['data'][0]['marker'] = dict(color=colors)

    return scatterplot


@callback(
    Output(component_id='scatterplot', component_property='figure', allow_duplicate=True),
    Input(component_id='projection-radio-buttons', component_property='value'),
    prevent_initial_call=True,
)
def radio_button_is_clicked(radio_button_value):
    print('radio_button_is_clicked')
    if radio_button_value == 't-SNE':
        x_col, y_col = 'tsne_x', 'tsne_y'
    elif radio_button_value == 'UMAP':
        x_col, y_col = 'umap_x', 'umap_y'

    fig = px.scatter(data_frame=Dataset.get(), x=x_col, y=y_col)
    fig.update_traces(customdata=Dataset.get().index)
    fig.update_layout(dragmode='select')

    return fig

@callback(
    [Output('wordcloud', 'src'),
    Output("table", "rowData"),
    Output("gallery", "children")],
    Input('scatterplot', 'selectedData'),
    prevent_initial_call=True,
)
def scatterplot_is_updated(selected_data):
    print('scatterplot_is_updated')
    if selected_data is None or not selected_data['points']:
        return '', [], []

    selected_image_ids = list(map(lambda point_data: point_data['customdata'], selected_data['points']))
    selected_data = Dataset.get().loc[selected_image_ids]
    group_by_count = selected_data.groupby(['class_id', 'class_name'])['class_id'].agg('count').to_frame('count_in_selection').reset_index()
    group_by_count['total_count'] = Dataset.class_count().loc[group_by_count['class_id']].values

    table_records = group_by_count.sort_values('count_in_selection', ascending=False).to_dict("records")

    counts = {row['class_name']: row['count_in_selection'] for _, row in group_by_count.iterrows()}
    img = BytesIO()
    wc = WordCloud(background_color='white', height=WORDCLOUD_IMAGE_HEIGHT, width=WORDCLOUD_IMAGE_WIDTH)
    wc.fit_words(counts)
    wc.to_image().save(img, format='PNG')
    wordcloud_image = encode_image(img.getvalue())

    sample_data = selected_data.head(IMAGE_GALLERY_SIZE)
    image_paths = sample_data['image_path'].values
    class_names = sample_data['class_name'].values
    image_rows = []
    for i in range(0, len(image_paths), IMAGE_GALLERY_ROW_SIZE):
        image_cols = []
        for j in range(IMAGE_GALLERY_ROW_SIZE):
            if i + j >= len(image_paths):
                break
            with open(image_paths[i+j], 'rb') as f:
                image = f.read()
            html_image = [
                html.Img(
                    src=encode_image(image),
                    className='gallery-image'
                ),
                html.Span(class_names[i+j], className='tooltip-text')
            ]
            image_cols.append(dbc.Col(html_image, width=3, className='gallery-row'))
        image_rows.append(dbc.Row(image_cols))

    return wordcloud_image, table_records, image_rows


def encode_image(image):
    return f'data:image/png;base64,{base64.b64encode(image).decode()}'

class Dataset:
    dataset = None
    count = None
    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(definitions.AUGMENTED_DATASET_PATH, index_col='image_id')
        Dataset.count = Dataset.data['class_id'].value_counts()

    @staticmethod
    def get():
        return Dataset.data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def files_exist():
        return os.path.isfile(definitions.AUGMENTED_DATASET_PATH) and os.path.isdir(definitions.IMAGES_DIR)

    @staticmethod
    def download():
        cub_loader.load()
        feature_engineering.generate_projection_data()

def main():
    if not Dataset.files_exist():
        print('File', definitions.AUGMENTED_DATASET_PATH, 'missing or directory', definitions.IMAGES_DIR, 'missing')
        print('Creating dataset')
        Dataset.download()
    Dataset.load()
    print('Starting Dash')
    run_ui()

if __name__ == '__main__':
    main()