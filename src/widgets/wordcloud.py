from io import BytesIO

from dash import html
from wordcloud import WordCloud
from src.utils import encode_image
from src import config


def create_wordcloud():
    return html.Img(id='wordcloud', className='border-widget')


def create_wordcloud_image(word_counts):
    if not word_counts:
        return ''
    img = BytesIO()
    wc = WordCloud(background_color='white', height=config.WORDCLOUD_IMAGE_HEIGHT, width=config.WORDCLOUD_IMAGE_WIDTH, random_state=1)
    wc.fit_words(word_counts)
    wc.to_image().save(img, format='PNG')
    return encode_image(img.getvalue())
