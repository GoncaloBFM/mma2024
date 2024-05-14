from dash import Output, Input, callback, Patch, State

from src import config
from src.widgets import graph, gallery, scatterplot


@callback(
    Output("grid", "dashGridOptions"),
    Input("table-filter", "value")
)
def table_filter_is_updated(filter_value):
    new_filter = Patch()
    new_filter['quickFilterText'] = filter_value
    return new_filter

@callback(
    [Output('wordcloud', 'list'),
     Output("gallery", "children"),
     Output("scatterplot", "figure"),
     Output("graph", "figure")],
    State('scatterplot', 'figure'),
    [Input("grid", "selectedRows"),
    Input("grid", "rowData")],
)
def table_row_is_selected(scatterplot_fig, selected_rows, added_rows):
    print('Table row selected')

    data_selected = scatterplot.get_data_selected_on_scatterplot(scatterplot_fig)
    scatterplot_fig['layout']['images'] = []

    if selected_rows:
        selected_classes = set(map(lambda row: row['class_id'], selected_rows))
        data_selected = data_selected[data_selected['class_id'].isin(selected_classes)]
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, selected_classes)
        wordcloud_data = [[row['class_name'], row['count_in_selection']] for row in selected_rows]
        graph_fig = graph.draw_graph(selected_rows)
    else:
        graph_fig = graph.draw_graph(None)
        group_by_count = (data_selected.groupby(['class_id', 'class_name'])['class_id']
                          .agg('count')
                          .to_frame('count_in_selection')
                          .reset_index())
        wordcloud_data = group_by_count[['class_name', 'count_in_selection']].values
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, None)

    sample_data = data_selected.sample(min(len(data_selected), config.IMAGE_GALLERY_SIZE), random_state=1)
    gallery_children = gallery.create_gallery_children(sample_data['image_path'].values, sample_data['class_name'].values)

    return wordcloud_data, gallery_children, scatterplot_fig, graph_fig

