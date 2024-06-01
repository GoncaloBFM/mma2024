from dash import html

from src import config
from dash_holoniq_wordcloud import DashWordcloud

def create_wordcloud():
    return html.Div(
        DashWordcloud(
            id='wordcloud',
            list=[],
            width=config.WORDCLOUD_IMAGE_WIDTH, height=config.WORDCLOUD_IMAGE_HEIGHT,
            shrinkToFit=True,
            drawOutOfBound=False,
            gridSize=16,
            backgroundColor='white',
            shuffle=False,
            rotateRatio=0.5,
            shape='square',
            hover=False,
            weightFactor=10,
        ),
        className='wordcloud-container border-widget stretchy-widget'
    )


def wordcloud_weight_rescale(series, dataset_min, dataset_max):
    return 1 + ((series - dataset_min) / (dataset_max - dataset_min)) * 9

