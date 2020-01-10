from . import webfrontend

import random
from pathlib import Path
from flask import render_template
from .constants import BRANDING_TAGLINES, RESULT_TAGS

GALLERY_IMGS = []
for comparison_dir in Path.cwd().glob("app/static/imgs/gallery/*"):
    if comparison_dir.is_dir():
        GALLERY_IMGS.append((
            f"imgs/gallery/{comparison_dir.name}/norm.jpg",
            f"imgs/gallery/{comparison_dir.name}/drag.jpg"
        ))

@webfrontend.route("/")
def main():
    """view method: landing page -- insert the gallery images and
    branding tagline"""
    return render_template(
        "frontend/app.html",
        gallery_imgs=GALLERY_IMGS,
        loadingLine="sending lerk to the cloud...",
        loadedLine=random.choice(RESULT_TAGS),
        branding_tagline=random.choice(BRANDING_TAGLINES),
    )