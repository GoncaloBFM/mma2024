import PIL.Image
from tqdm import tqdm
import clip
import torch
import pandas
import numpy
from umap import UMAP
from sklearn.manifold import TSNE

from src import config



def calculate_clip_embeddings(dataset):
    model, preprocess = clip.load('ViT-B/32', device='cpu')
    clip_embeddings = []
    for image_name in tqdm(dataset['image_path']):
        image = PIL.Image.open(image_name)
        image_input = preprocess(image).unsqueeze(0).to('cpu')
        with torch.no_grad():
            clip_embeddings.append(model.encode_image(image_input).cpu().numpy())
    clip_embeddings = numpy.concatenate(clip_embeddings, axis=0)
    return clip_embeddings


def calculate_umap(clip_embeddings):
    umap_embeddings = UMAP(metric='cosine', n_components=2).fit_transform(clip_embeddings)
    umap_x, umap_y = umap_embeddings[:, 0], umap_embeddings[:, 1]
    return umap_x, umap_y


def calculate_tsne(clip_embeddings):
    tsne_embeddings = TSNE(metric='cosine', n_components=2).fit_transform(clip_embeddings)
    tsne_x, tsne_y = tsne_embeddings[:, 0], tsne_embeddings[:, 1]
    return tsne_x, tsne_y


def generate_projection_data():
    dataset = pandas.read_csv(config.DATASET_PATH)
    dataset_sample = dataset.sample(n=config.DATASET_SAMPLE_SIZE, random_state=1) if config.DATASET_SAMPLE_SIZE else dataset
    print('Calculating clip embeddings')
    clip_embeddings = calculate_clip_embeddings(dataset_sample)
    umap_x, umap_y = calculate_umap(clip_embeddings)
    print('Calculating umap')
    tsne_x, tsne_y = calculate_tsne(clip_embeddings)
    print('Calculating tsne')
    augmented_dataset = dataset_sample.assign(umap_x=umap_x, umap_y=umap_y, tsne_x=tsne_x, tsne_y=tsne_y)
    augmented_dataset.to_csv(config.AUGMENTED_DATASET_PATH, index=False)
    print('Saving augmented dataset to', config.AUGMENTED_DATASET_PATH)


if __name__ == '__main__':
    generate_projection_data()
