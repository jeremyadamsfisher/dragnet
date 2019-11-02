import typing as t
import numpy as np
import PIL
from PIL.Image import Image
from .face_evolve import detect_faces

def translate_face(img: Image) -> Image:
    raise NotImplementedError

def translate(img: Image) -> Image:
    """extract the face out from an image, get it into drag"""
    bounding_boxes, _ = detect_faces(img)
    x1, y1, x2, y2, *_ = bounding_boxes[0].astype(np.uint32)
    img_face = img.crop((x1, y1, x2, y2))
    face_img_drag = PIL.Image.new('RGBA', (int(x2-x1), int(y2-y1)), (255, 255, 255, 255))
    #face_img_drag = translate_face(img_face)
    img.paste(face_img_drag, (x1, y1))
    return img
