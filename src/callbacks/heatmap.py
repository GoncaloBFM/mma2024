from dash import callback, Output, Input, html, no_update

from src.utils import encode_image

@callback(
    Output("heatmap-tooltip", "show"),
    Output("heatmap-tooltip", "bbox"),
    Output("heatmap-tooltip", "children"),
    Input("heatmap", "hoverData"), 
)
def display_hover(hover_data):
    print('Heatmap is hovered')
    if hover_data is None:
        return False, no_update, no_update

    pt = hover_data["points"][0]
    bbox = pt["bbox"]
    x = pt["x"]
    y = pt["y"]
    z = pt["z"]

    bird_name = y.split('/')[-2].split('.')[1].replace('_', ' ')
    image_path = y

    with open(image_path, 'rb') as f:
        image = f.read()

    content = [
        html.Img(src=encode_image(image), style={"width": "100%"}), 
        html.P(bird_name, style={"font-weight": "bold", "font-size": "14px"}),
    ]
    if z > 0: 
        certainty = '(guessing)' if z == 1 else '(probably)' if z == 2 else '(definitely)'
        content.append(html.P(x + ' ' + certainty, style={"font-style": "italic", "font-size": "14px"}))

    children = [
        html.Div(content, style={'width': '150px', 'white-space': 'normal'})
    ]

    return True, bbox, children

@callback(
    Output("grid", "selectedRows", allow_duplicate=True),
    Input("heatmap", "clickData"),
    prevent_initial_call=True,
)
def heatmap_is_clicked(click_data):
    print('Heatmap is clicked')
    class_name = click_data['points'][0]['y'].split('/')[-2].split('.')[1].replace('_', ' ')
    return {'function': f'params.data.class_name == "{class_name}"'}