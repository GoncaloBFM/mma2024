import base64
import os.path
from io import BytesIO

import dash
import dash_ag_grid

import plotly.express as px
from PIL import Image
from wordcloud import WordCloud

from src import definitions
from src.Dataset import Dataset
from dash import Dash, html, dcc, Output, Input, callback, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

IMAGE_GALLERY_SIZE = 36
IMAGE_GALLERY_ROW_SIZE = 4

WORDCLOUD_IMAGE_HEIGHT = 450
WORDCLOUD_IMAGE_WIDTH = 600

SCATTERPLOT_COLOR = 'rgba(31, 119, 180, 0.5)'
SCATTERPLOT_SELECTED_COLOR = 'red'

DEFAULT_PROJECTION = 'UMAP'
MAX_IMAGES_ON_SCATTERPLOT = 15


def run_ui():
    external_stylesheets = [dbc.themes.CERULEAN]
    app = Dash(__name__, external_stylesheets=external_stylesheets)

    projection_radio_buttons = dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['t-SNE', 'UMAP']],
        value=DEFAULT_PROJECTION,
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
        className='widget ag-theme-alpine',
        style={'width': '', 'height': ''},
        id='table'
    )

    scatterplot_figure = radio_button_is_clicked(DEFAULT_PROJECTION)

    scatterplot = dcc.Graph(
        figure=scatterplot_figure,
        id='scatterplot',
        className='widget',
        config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['resetScale'],
            'displayModeBar': True,
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
        colors = Dataset.get()['class_id'].map(lambda x: SCATTERPLOT_SELECTED_COLOR if selected_class == x else SCATTERPLOT_COLOR)
    else:
        colors = 'blue'

    scatterplot['data'][0]['marker'] = dict(color=colors)

    return scatterplot


@callback(
    Output('scatterplot', 'figure'),
    State('scatterplot', 'figure'),
    Input('scatterplot', 'relayoutData'),
    prevent_initial_call=True,
)
def scatterplot_is_zoomed(scatterplot, zoom_data):
    if len(zoom_data) == 1 and 'dragmode' in zoom_data:
        return dash.no_update

    scatterplot['layout']['images'] = []

    if 'xaxis.range[0]' not in zoom_data:
        return scatterplot

    print('scatter_plot_is_zoomed')
    fig = go.Figure(scatterplot)
    scatterplot_data = scatterplot['data'][0]
    scatter_image_ids = scatterplot_data['customdata']
    scatter_x = scatterplot_data['x']
    scatter_y = scatterplot_data['y']
    min_x = zoom_data['xaxis.range[0]']
    max_x = zoom_data['xaxis.range[1]']
    min_y = zoom_data['yaxis.range[0]']
    max_y = zoom_data['yaxis.range[1]']
    images_in_zoom = []
    for x, y, image_id in zip(scatter_x, scatter_y, scatter_image_ids):
        if min_x <= x <= max_x and min_y <= y <= max_y:
            images_in_zoom.append((x, y, image_id))
        if len(images_in_zoom) > MAX_IMAGES_ON_SCATTERPLOT:
            return fig

    if images_in_zoom:
        fig = go.Figure(scatterplot)
        for x, y, image_id in images_in_zoom:
            image_path = Dataset.get().loc[image_id]['image_path']
            fig.add_layout_image(
                x=x,
                y=y,
                source=Image.open(image_path),
                xref="x",
                yref="y",
                sizex=.05,
                sizey=.05,
                xanchor="center",
                yanchor="middle",
            )
        return fig

    return fig

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
    fig.update_traces(customdata=Dataset.get().index, marker={'color':SCATTERPLOT_COLOR})
    fig.update_layout(dragmode='select')
    fig.update_yaxes(scaleanchor="x", scaleratio=1)

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
    group_by_count = selected_data.groupby(['class_id', 'class_name'])['class_id'].agg('count').to_frame(
        'count_in_selection').reset_index()
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
            with open(image_paths[i + j], 'rb') as f:
                image = f.read()
            class_name = class_names[i + j]
            html_image = [html.A([
                html.Img(
                    src=encode_image(image),
                    className='gallery-image'
                ),
                html.Span(class_name, className='tooltip-text')
            ], target="_blank", href=f'http://www.google.com/search?q={class_name.replace(" ", "+")}')]
            image_cols.append(dbc.Col(html_image, width=3, className='gallery-row'))
        image_rows.append(dbc.Row(image_cols))

    return wordcloud_image, table_records, image_rows


def encode_image(image):
    source = f'data:image/png;base64,{base64.b64encode(image).decode()}'
    return source


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
