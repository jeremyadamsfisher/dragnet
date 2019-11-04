"""tie together cyclegan and face.evoLVe"""

import typing as t
import numpy as np
import PIL
from PIL.Image import Image
from .face_evolve import detect_faces
from .cyclegan import translate_face_subimage


def translate(img: Image) -> Image:
    """extract the face out from an image, get it into drag"""
    # 
    x, y = img.size
    minor_axis, major_axis = sorted(img.size)
    scale_factor = 512 / major_axis
    x_scaled = int(x * scale_factor)
    y_scaled = int(y * scale_factor)
    thumb = img.copy()
    thumb.thumbnail((x_scaled, y_scaled), PIL.Image.ANTIALIAS)

    bounding_boxes, _ = detect_faces(thumb)
    
    if len(bounding_boxes) == 0:
        raise ValueError
    
    for bounding_box in bounding_boxes:
        b = bounding_box.astype(np.uint32)
        b = [int(x / scale_factor) for x in b]
        x1, y1, x2, y2, *_ = b
        width = x2-x1
        height = y2-y1
        size = min((width, height)) // 0.75
        img_face = img.crop((x1, y1, x1+size, y1+size))
        face_img_drag = translate_face_subimage(img_face)
        face_img_drag.thumbnail((size, size), PIL.Image.ANTIALIAS)
        img.paste(face_img_drag, (x1, y1))

    # downscale to make the transmission back quick
    img.thumbnail((x_scaled, y_scaled), PIL.Image.ANTIALIAS)

    return img
