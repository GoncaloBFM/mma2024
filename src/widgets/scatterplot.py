from PIL import Image
from dash import dcc
import plotly.express 
from src.Dataset import Dataset
from src import config
import plotly.graph_objects as go


def highlight_class_on_scatterplot(scatterplot, class_ids):
    if class_ids:
        colors = Dataset.get()['class_id'].map(lambda x: config.SCATTERPLOT_SELECTED_COLOR if x in class_ids else config.SCATTERPLOT_COLOR)
    else:
        colors = config.SCATTERPLOT_COLOR
    scatterplot['data'][0]['marker'] = {'color': colors}


def add_images_to_scatterplot(scatterplot_fig):
    scatterplot_fig['layout']['images'] = []
    scatterplot_data = scatterplot_fig['data'][0]
    scatter_image_ids = scatterplot_data['customdata']
    scatter_x = scatterplot_data['x']
    scatter_y = scatterplot_data['y']

    min_x, max_x = scatterplot_fig['layout']['xaxis']['range']
    min_y, max_y = scatterplot_fig['layout']['yaxis']['range']

    images_in_zoom = []
    for x, y, image_id in zip(scatter_x, scatter_y, scatter_image_ids):
        if min_x <= x <= max_x and min_y <= y <= max_y:
            images_in_zoom.append((x, y, image_id))
        if len(images_in_zoom) > config.MAX_IMAGES_ON_SCATTERPLOT:
            return scatterplot_fig

    if images_in_zoom:
        for x, y, image_id in images_in_zoom:
            image_path = Dataset.get().loc[image_id]['image_path']
            scatterplot_fig['layout']['images'].append(dict(
                x=x,
                y=y,
                source=Image.open(image_path),
                xref="x",
                yref="y",
                sizex=.05,
                sizey=.05,
                xanchor="center",
                yanchor="middle",
            ))
        return scatterplot_fig
    return scatterplot_fig


def create_scatterplot_figure(projection):
    if projection == 't-SNE':
        x_col, y_col = 'tsne_x', 'tsne_y'
    elif projection == 'UMAP':
        x_col, y_col = 'umap_x', 'umap_y'
    else:
        raise Exception('Projection not found')

    fig = plotly.express.scatter(data_frame=Dataset.get(), x=x_col, y=y_col)
    fig.update_traces(
        customdata=Dataset.get().index, 
        marker={'color': config.SCATTERPLOT_COLOR},
        unselected_marker_opacity=0.60)
    fig.update_layout(dragmode='select')
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            name='image embedding',
            marker=dict(size=7, color="blue", symbol='circle'),
        ),
    )
    fig.add_trace(
        go.Scatter(
            x=[None],
            y=[None],
            mode="markers",
            name='selected class',
            marker=dict(size=7, color="red", symbol='circle'),
        ),
    )

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="left",
        x=0
    ))
    return fig


def create_scatterplot(projection):
    return dcc.Graph(
            figure=create_scatterplot_figure(projection),
            id='scatterplot',
            className='stretchy-widget border-widget',
            responsive=True,
            config={
                'displaylogo': False,
                'modeBarButtonsToRemove': ['autoscale'],
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


