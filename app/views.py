import os
import random
from pathlib import Path
from flask import render_template

from .constants import BRANDING_TAGLINES, TAGS
from app import app

GALLERY_IMGS = []
for comparison_dir in Path("./app/static/imgs").glob("*"):
    if comparison_dir.is_dir():
        GALLERY_IMGS.append((
            f"imgs/{comparison_dir.name}/norm.jpg",
            f"imgs/{comparison_dir.name}/drag.jpg"
        ))

@app.route("/")
def main():
    """view method: landing page -- insert the gallery images and
    branding tagline"""
    return render_template(
        "main.html",
        gallery_imgs=GALLERY_IMGS,
        branding_tagline=random.choice(BRANDING_TAGLINES),
    )


@app.route("/result/<img_id>")
def result(img_id: str):
    """render the result of the person in drag"""
    return render_template(
        "result.html",
        tag=random.choice(TAGS)
    )
