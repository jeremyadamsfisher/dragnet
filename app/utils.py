import PIL
from PIL.Image import Image

def resize_image(img: Image, max_size=512) -> Image:
    """resize an image such that its major axis is
    no larger than specified
    """
    x, y = img.size
    major_axis = max((x, y))
    scale_factor = 512 / major_axis
    x_scaled = int(x * scale_factor)
    y_scaled = int(y * scale_factor)
    img.thumbnail((x_scaled, y_scaled), PIL.Image.ANTIALIAS)
    return img
