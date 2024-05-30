from dash import callback, Output, Input, State, dash
from PIL import Image
from src import config

from src.Dataset import Dataset
from src.widgets import scatterplot


@callback(
    Output('scatterplot', 'figure', allow_duplicate=True),
    State('scatterplot', 'figure'),
    Input('scatterplot', 'relayoutData'),
    prevent_initial_call=True,
)
def scatterplot_is_zoomed(scatterplot_fig, zoom_data):
    if len(zoom_data) == 1 and 'dragmode' in zoom_data:
        return dash.no_update

    scatterplot_fig['layout']['images'] = []

    if 'xaxis.range[0]' not in zoom_data:
        return scatterplot_fig

    print('Scatterplot is zoomed')
    scatterplot_data = scatterplot_fig['data'][0]
    scatter_image_ids = scatterplot_data['customdata']
    scatter_x = scatterplot_data['x']
    scatter_y = scatterplot_data['y']
    min_x = zoom_data['xaxis.range[0]']
    max_x = zoom_data['xaxis.range[1]']
    min_y = zoom_data['yaxis.range[0]']
    max_y = zoom_data['yaxis.range[1]']
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


@callback(
    Output("grid", "rowData"),
    State('scatterplot', 'figure'),
    Input("scatterplot", "selectedData"),
)
def scatterplot_is_selected(scatterplot_fig, data_selected):
    print('Scatterplot is selected')

    data_selected = scatterplot.get_data_selected_on_scatterplot(scatterplot_fig)
    scatterplot_fig['layout']['images'] = []

    group_by_count = (data_selected.groupby(['class_id', 'class_name'])['class_id']
                          .agg('count')
                          .to_frame('count_in_selection')
                          .reset_index())
    group_by_count['total_count'] = Dataset.class_count().loc[group_by_count['class_id']].values
    table_rows = group_by_count.sort_values('count_in_selection', ascending=False).to_dict("records")
    scatterplot.highlight_class_on_scatterplot(scatterplot_fig, None)

    return table_rows


