import dash_bootstrap_components as dbc
from dash import html

from src import config
from src.utils import encode_image


def create_gallery():
    return dbc.Card(
        [
            dbc.CardHeader(f'Sample of images from selection'),
            dbc.CardBody([], id='gallery', className='gallery widget'),
        ],
        className='stretchy-widget border-widget'
    )


def create_gallery_children(image_paths, class_names):
    image_rows = []
    for i in range(0, len(image_paths), config.IMAGE_GALLERY_ROW_SIZE):
        image_cols = []
        for j in range(config.IMAGE_GALLERY_ROW_SIZE):
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
                html.Div(class_name, className='gallery-text')
            ], target="_blank", href=f'http://www.google.com/search?q={class_name.replace(" ", "+")}')]
            image_cols.append(dbc.Col(html_image, className='gallery-col'))
        image_rows.append(dbc.Row(image_cols, className='gallery-row', justify='start'))

    return image_rows