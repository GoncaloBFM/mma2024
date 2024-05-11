from dash import Output, Input, callback, Patch

@callback(
    Output("grid", "dashGridOptions"),
    Input("table-filter", "value")
)
def table_filter_is_updated(filter_value):
    new_filter = Patch()
    new_filter['quickFilterText'] = filter_value
    return new_filter
