import os
from pathlib import Path

# ui configuration
IMAGE_GALLERY_SIZE = 24
IMAGE_GALLERY_ROW_SIZE = 4

WORDCLOUD_IMAGE_HEIGHT = 600
WORDCLOUD_IMAGE_WIDTH = 800

SCATTERPLOT_COLOR = 'rgba(31, 119, 180, 0.5)'
SCATTERPLOT_SELECTED_COLOR = 'red'

MAX_IMAGES_ON_SCATTERPLOT = 100

DEFAULT_PROJECTION = 'UMAP'
DEFAULT_LEFT_WIDGET = 'table'

MAX_GRAPH_NODES = 12

# dataset extraction configuration
DATASET_SAMPLE_SIZE = 1000 # number of images in the CUB-200-2011 dataset is 11788, that is the max value for this parameter


# path configuration
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, 'dataset')
DATA_DIR = os.path.join(DATASET_DIR, 'data')
DOWNLOADS_DIR = os.path.join(DATASET_DIR, 'downloads')
DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
AUGMENTED_DATASET_PATH = os.path.join(DATA_DIR, 'augmented_dataset.csv')
ATTRIBUTE_DATA_PATH = os.path.join(DATA_DIR, 'image_attributes.csv')
