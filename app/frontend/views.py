from . import webfrontend

import random
from pathlib import Path
from flask import (
    render_template,
    make_response,
    jsonify
)
from .constants import (
    BRANDING_TAGLINES,
    UPLOADINGS_TAGS,
    PREDICTING_TAGS,
    RESULT_TAGS,
)

GALLERY_IMGS = [
    (f"imgs/gallery/{comparison_dir.name}/norm.jpg",
     f"imgs/gallery/{comparison_dir.name}/drag.jpg")
    for comparison_dir
    in Path.cwd().glob("app/static/imgs/gallery/*")
]

@webfrontend.route("/")
def main():
    """view method: landing page -- insert the gallery images and
    branding tagline"""
    return render_template(
        "frontend/app.html",
        gallery_imgs=GALLERY_IMGS,
        branding_tagline=random.choice(BRANDING_TAGLINES),
    )


@webfrontend.route("/quip/<quiptype>")
def get_quip(quiptype):
    if quiptype == "uploading":
        quip = random.choice(UPLOADINGS_TAGS)
    elif quiptype == "predicting":
        quip = random.choice(PREDICTING_TAGS)
    elif quiptype == "done":
        quip = random.choice(RESULT_TAGS)
    else:
        raise ValueError
    return make_response(jsonify({"quip": quip}), 200)