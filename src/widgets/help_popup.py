import dash_bootstrap_components as dbc

from src import config


def create_help_popup():
    return dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("How to use")),
            dbc.ModalBody('With this tool you can explore the CUB-200-2011 through a 2D UMAP or t-SNE projection of the CLIP embeddings of the bird images in the dataset. '),
            dbc.ModalBody('Use the scatterplot to select instances of bird images. '
                          'Click on the scatterplot icons above the scatterplot to select mode of use. '
                          'Double click on scatterplot selections while using the select tool to deselect.'),
            dbc.ModalBody('Use the table to select bird species. The table rows can be filtered by clicking the hamburgers on the table hearder. '
                          'Mouse click to select a row. '
                          'Use Crtl + click to select multiple rows and deselect rows. '
                          'Use Shift + click to select blocks of rows. '),
            dbc.ModalBody(f'Use the widgets in the tabs to explore the data. The gallery shows you a sample of up to {config.IMAGE_GALLERY_SIZE} images. '
                          f'The graph shows birds with the same last species name considering up to {config.MAX_GRAPH_NODES} central nodes. '
                          'The wordcloud and histogram show the most prevalent bird species in a selection. '
                          'The heatmap shows different characteristics per bird image.'),
        ],
        id="help-popup",
        is_open=False,
    )
