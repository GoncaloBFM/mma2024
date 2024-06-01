import dash
import numpy
from dash import Output, Input, callback, Patch, State
from dash.exceptions import PreventUpdate

from src import config, utils
from src.Dataset import Dataset
from src.widgets import graph, gallery, scatterplot, histogram, heatmap, wordcloud


@callback(
    [Output('wordcloud', 'list'),
     Output("gallery", "children"),
     Output("scatterplot", "figure"),
     Output("graph", "figure"), 
     Output('histogram', 'figure'), 
     Output("heatmap", "figure"), ],
    State('scatterplot', 'figure'),
    [Input("grid", "selectedRows"),
    Input("grid", "rowData")],
)
def table_row_is_selected(scatterplot_fig, selected_rows, added_rows):
    if type(selected_rows) is dict:
        raise PreventUpdate()

    print('Table row selected')

    data_selected = scatterplot.get_data_selected_on_scatterplot(scatterplot_fig)
    scatterplot_fig['layout']['images'] = []

    if selected_rows:
        classes_in_scatterplot = data_selected['class_name'].unique()
        selected_classes = set(map(lambda row: row['class_id'], selected_rows))
        data_selected = data_selected[data_selected['class_id'].isin(selected_classes)]
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, selected_classes)
        wordcloud_data = [[row['class_name'], count] for row, count in zip(
            selected_rows,
            wordcloud.wordcloud_weight_rescale(
                numpy.array([row['count_in_selection'] for row in selected_rows]),
                1,
                Dataset.class_count().max())
        )]
        graph_fig = graph.draw_graph(selected_rows[:config.MAX_GRAPH_NODES], valid_birds=classes_in_scatterplot)
    else:
        group_by_count = (data_selected.groupby(['class_id', 'class_name'])['class_id']
                          .agg('count')
                          .to_frame('count_in_selection')
                          .reset_index())

        group_by_count['count_in_selection'] = wordcloud.wordcloud_weight_rescale(
            group_by_count['count_in_selection'],
            1,
            Dataset.class_count().max())
        wordcloud_data = group_by_count[['class_name', 'count_in_selection']].values
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, None)
        graph_input = [{"class_name": class_name} for class_name in data_selected.sample(min(config.MAX_GRAPH_NODES, len(data_selected)))['class_name'].values]
        graph_fig = graph.draw_graph(graph_input, drag_select=True)

    sample_data = data_selected.sample(min(len(data_selected), config.IMAGE_GALLERY_SIZE), random_state=1)
    gallery_children = gallery.create_gallery_children(sample_data['image_path'].values, sample_data['class_name'].values)

    histogram_fig = histogram.draw_histogram(selected_data=data_selected)

    heatmap_fig = heatmap.draw_heatmap_figure(data_selected)

    return wordcloud_data, gallery_children, scatterplot_fig, graph_fig, histogram_fig, heatmap_fig
