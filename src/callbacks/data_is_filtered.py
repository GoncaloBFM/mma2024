import dash
from dash import Input, Output, State, callback

from src import config
from src.Dataset import Dataset
from src.widgets import wordcloud, gallery, scatterplot, graph, heatmap


@callback(
    [Output('wordcloud', 'src'),
     Output("grid", "rowData"),
     Output("gallery", "children"),
     Output('scatterplot', 'figure'),
     Output("graph", "figure"), 
     Output("heatmap", "figure")],
    State('scatterplot', 'figure'),
    [Input('scatterplot', 'selectedData'),
    Input("grid", "selectedRows")]
)
def data_is_filtered(scatterplot_fig, scatterplot_selection, table_selection):
    print('Data is filtered using', dash.ctx.triggered_id)

    data_selected = get_data_selected_on_scatterplot(scatterplot_fig)
    scatterplot_fig['layout']['images'] = []

    if ((dash.ctx.triggered_id == 'scatterplot' or dash.ctx.triggered_id is None)
            or (dash.ctx.triggered_id == 'grid' and not table_selection)):
        group_by_count = (data_selected.groupby(['class_id', 'class_name'])['class_id']
                          .agg('count')
                          .to_frame('count_in_selection')
                          .reset_index())
        group_by_count['total_count'] = Dataset.class_count().loc[group_by_count['class_id']].values
        table_rows = group_by_count.sort_values('count_in_selection', ascending=False).to_dict("records")
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, None)
        class_counts = {row['class_name']: row['count_in_selection'] for _, row in group_by_count.iterrows()}
        graph_fig = graph.draw_graph(table_selection)

    elif dash.ctx.triggered_id == 'grid' and table_selection:
        selected_classes = set(map(lambda row: row['class_id'], table_selection))
        data_selected = data_selected[data_selected['class_id'].isin(selected_classes)]
        scatterplot.highlight_class_on_scatterplot(scatterplot_fig, selected_classes)
        class_counts = {row['class_name']: row['count_in_selection'] for row in table_selection}
        table_rows = dash.no_update
        graph_fig = graph.draw_graph(table_selection)

    else:
        raise Exception(f'Unknown id triggered the callback: {dash.ctx.triggered_id}')

    wordcloud_image = wordcloud.create_wordcloud_image(class_counts)

    sample_data = data_selected.sample(min(len(data_selected), config.IMAGE_GALLERY_SIZE), random_state=1)
    gallery_children = gallery.create_gallery_children(sample_data['image_path'].values, sample_data['class_name'].values)

    heatmap_fig = heatmap.draw_heatmap_figure(data_selected)

    return wordcloud_image, table_rows, gallery_children, scatterplot_fig, graph_fig, heatmap_fig


def get_data_selected_on_scatterplot(scatterplot_fig):
    scatterplot_fig_data = scatterplot_fig['data'][0]

    if 'selectedpoints' in scatterplot_fig_data:
        selected_image_ids = list(map(scatterplot_fig_data['customdata'].__getitem__, scatterplot_fig_data['selectedpoints']))
        data_selected = Dataset.get().loc[selected_image_ids]
    else:
        data_selected = Dataset.get()

    return data_selected
