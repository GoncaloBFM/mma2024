import os
from pathlib import Path
ROOT_DIR = Path(__file__).parent.parent
DATASET_DIR = os.path.join(ROOT_DIR, 'dataset')
DATA_DIR = os.path.join(DATASET_DIR, 'data')
DOWNLOADS_DIR = os.path.join(DATASET_DIR, 'downloads')
DATASET_PATH = os.path.join(DATA_DIR, 'dataset.csv')
IMAGES_DIR = os.path.join(DATA_DIR, 'images')
AUGMENTED_DATASET_PATH = os.path.join(DATA_DIR, 'augmented_dataset.csv')
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.ini')

