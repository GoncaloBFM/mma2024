import dash_bootstrap_components as dbc
from src import config


def create_projection_radio_buttons():
    return dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['UMAP', 't-SNE']],
        value=config.DEFAULT_PROJECTION,
        inline=True,
        id='projection-radio-buttons',
        class_name='radio-buttons'
    )