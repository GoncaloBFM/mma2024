# from dash import callback, Output, Input, html, no_update

# from src.utils import encode_image

# @callback(
#     Output("heatmap-tooltip", "show"),
#     Output("heatmap-tooltip", "bbox"),
#     Output("heatmap-tooltip", "children"),
#     Input("heatmap", "hoverData"), 
# )
# def display_hover(hoverData): 
#     print('display_hover')
#     if hoverData is None:
#         return False, no_update, no_update

#     pt = hoverData["points"][0]
#     bbox = pt["bbox"]
#     x = pt["x"]
#     y = pt["y"]
#     z = pt["z"]

#     bird_name = y.split('/')[-2].split('.')[1].replace('_', ' ')
#     image_path = y

#     with open(image_path, 'rb') as f:
#         image = f.read()

#     content = [
#         html.Img(src=encode_image(image), style={"width": "100%"}), 
#         html.P(bird_name, style={"font-weight": "bold", "font-size": "14px"}),
#     ]
#     if z > 0: 
#         certainty = '(guessing)' if z == 1 else '(probably)' if z == 2 else '(definitely)'
#         content.append(html.P(x + ' ' + certainty, style={"font-style": "italic", "font-size": "14px"}))

#     children = [
#         html.Div(content, style={'width': '150px', 'white-space': 'normal'})
#     ]

#     return True, bbox, children