import os

import pandas

from src import config, feature_engineering
from src.dataloaders import cub_loader


class Dataset:
    data = None
    count = None
    attr_data = None
    @staticmethod
    def load():
        Dataset.data = pandas.read_csv(config.AUGMENTED_DATASET_PATH, index_col='image_id')
        Dataset.count = Dataset.data['class_id'].value_counts()
        Dataset.data['species_name'] = Dataset.data['class_name'].apply(lambda x: x.split()[-1])
        Dataset.attr_data = pandas.read_csv(config.ATTRIBUTE_DATA_PATH, index_col='image_id')

    @staticmethod
    def get():
        return Dataset.data
    
    @staticmethod
    def get_attr_data():
        return Dataset.attr_data

    @staticmethod
    def class_count():
        return Dataset.count

    @staticmethod
    def files_exist():
        return os.path.isfile(config.AUGMENTED_DATASET_PATH) and os.path.isdir(config.IMAGES_DIR) and os.path.isfile(config.ATTRIBUTE_DATA_PATH)

    @staticmethod
    def download():
        cub_loader.load()
        feature_engineering.generate_projection_data()
        cub_loader.cleanup()