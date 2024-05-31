import dash_bootstrap_components as dbc
from dash import html

from src import config
from src.utils import encode_image


def create_gallery():
    return html.Div([], id='gallery', className='stretchy-widget border-widget gallery')

def create_gallery_children(image_paths, class_names):
    image_rows = []
    image_id = 0
    for i in range(0, len(image_paths), config.IMAGE_GALLERY_ROW_SIZE):
        image_cols = []
        for j in range(config.IMAGE_GALLERY_ROW_SIZE):
            if i + j >= len(image_paths):
                break
            with open(image_paths[i + j], 'rb') as f:
                image = f.read()
            class_name = class_names[i + j]
            html_card = html.A([
                    html.Img(src=encode_image(image),className='gallery-image'),
                    html.Div(class_name, className='gallery-text')
                ], id={'type': 'gallery-card', 'index': class_name}, className='gallery-card'
            )
            image_cols.append(dbc.Col(html_card, className='gallery-col', width=3))
            image_id += 1
        image_rows.append(dbc.Row(image_cols, className='gallery-row', justify='start'))

    return image_rows
