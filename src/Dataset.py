import os

import pandas

from src import definitions, feature_engineering
from src.dataloader import cub_loader


class Dataset:
    dataset = None
    count = None
    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(definitions.AUGMENTED_DATASET_PATH, index_col='image_id')
        Dataset.count = Dataset.data['class_id'].value_counts()

    @staticmethod
    def get():
        return Dataset.data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def files_exist():
        return os.path.isfile(definitions.AUGMENTED_DATASET_PATH) and os.path.isdir(definitions.IMAGES_DIR)

    @staticmethod
    def download():
        cub_loader.load()
        feature_engineering.generate_projection_data()
        cub_loader.cleanup()
