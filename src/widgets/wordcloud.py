from io import BytesIO

from dash import html
from wordcloud import WordCloud
from src.utils import encode_image
from src import config
from dash_holoniq_wordcloud import DashWordcloud

def create_wordcloud():
    return DashWordcloud(
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
        hover=True,
        weightFactor=10
    )