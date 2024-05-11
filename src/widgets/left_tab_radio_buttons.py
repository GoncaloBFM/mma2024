import dash_bootstrap_components as dbc
from src import config

from src import config

def create_left_tab_radio_buttons():
    return dbc.RadioItems(
        options=[{"label": x, "value": x} for x in ['table', 'placeholder']],
        value=config.DEFAULT_LEFT_WIDGET,
        inline=True,
        id='left-tab-radio-buttons',
        class_name='radio-buttons'
    )