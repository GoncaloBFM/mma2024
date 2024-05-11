import base64

def encode_image(image):
    source = f'data:image/png;base64,{base64.b64encode(image).decode()}'
    return source

