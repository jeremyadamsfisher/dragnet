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
        x1, y1, x2, y2, *_ = bounding_box.astype(np.uint32)
        width, height = x2 - x1, y2 - y1
        s = min((width, height)) // 0.75
        img_face = img.crop((x1, y1, x1 + s, y1 + s))
        face_img_drag = translate_face_subimage(img_face)
        img.paste(face_img_drag, (x1, y1))

    return img
