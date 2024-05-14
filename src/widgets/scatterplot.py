from dash import dcc
import plotly.express 
from src.Dataset import Dataset
from src import config


def highlight_class_on_scatterplot(scatterplot, class_ids):
    if class_ids:
        colors = Dataset.get()['class_id'].map(lambda x: config.SCATTERPLOT_SELECTED_COLOR if x in class_ids else config.SCATTERPLOT_COLOR)
    else:
        colors = config.SCATTERPLOT_COLOR
    scatterplot['data'][0]['marker'] = {'color': colors}


def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'tsne_x', 'tsne_y'
    elif projection == 'UMAP':
        x_col, y_col = 'umap_x', 'umap_y'
    else:
        raise Exception('Projection not found')

    fig = plotly.express.scatter(data_frame=Dataset.get(), x=x_col, y=y_col)
    fig.update_traces(customdata=Dataset.get().index, marker={'color': config.SCATTERPLOT_COLOR})
    fig.update_layout(dragmode='select')
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot',
            className='stretchy-widget',
            responsive=True,
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['resetScale'],
                'displayModeBar': True,
            }
        )

def get_data_selected_on_scatterplot(scatterplot_fig):
    scatterplot_fig_data = scatterplot_fig['data'][0]

    if 'selectedpoints' in scatterplot_fig_data:
        selected_image_ids = list(map(scatterplot_fig_data['customdata'].__getitem__, scatterplot_fig_data['selectedpoints']))
        data_selected = Dataset.get().loc[selected_image_ids]
    else:
        data_selected = Dataset.get()

    return data_selected


