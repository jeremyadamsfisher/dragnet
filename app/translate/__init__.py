"""tie together cyclegan and face.evoLVe"""

import typing as t
import numpy as np
import PIL
from PIL.Image import Image
from .face_evolve import detect_faces
from .cyclegan import translate_face_subimage

def translate(img: Image) -> Image:
    """extract the face out from an image, get it into drag"""
    bounding_boxes, _ = detect_faces(img)
    if len(bounding_boxes) == 0:
        raise ValueError
    for bounding_box in bounding_boxes:
        b = bounding_box.astype(np.uint32)
        x1, y1, x2, y2, *_ = b
        width = x2-x1
        height = y2-y1
        size = min((width, height)) // 0.75
        img_face = img.crop((x1, y1, x1+size, y1+size))
        face_img_drag = translate_face_subimage(img_face)
        face_img_drag.thumbnail((size, size), PIL.Image.ANTIALIAS)
        img.paste(face_img_drag, (x1, y1))
    return img
