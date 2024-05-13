import os

import pandas

from src import config, feature_engineering
from src.dataloader import cub_loader


class Dataset:
    data = None
    count = None
    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(config.AUGMENTED_DATASET_PATH, index_col='image_id')
        Dataset.count = Dataset.data['class_id'].value_counts()
        Dataset.data['species_name'] = Dataset.data['class_name'].apply(lambda x: x.split()[-1])

    @staticmethod
    def get():
        return Dataset.data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def files_exist():
        return os.path.isfile(config.AUGMENTED_DATASET_PATH) and os.path.isdir(config.IMAGES_DIR)

    @staticmethod
    def download():
        cub_loader.load()
        feature_engineering.generate_projection_data()
        cub_loader.cleanup()
