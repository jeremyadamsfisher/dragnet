import random
from pathlib import Path
from flask import render_template, Blueprint

from .constants import BRANDING_TAGLINES, RESULT_TAGS

webfrontend = Blueprint(
    "frontend",
    __name__,
    template_folder="templates",
    static_folder="static"
)

GALLERY_IMGS = []
for comparison_dir in Path("./app/static/frontend/imgs").glob("*"):
    if comparison_dir.is_dir():
        GALLERY_IMGS.append((
            f"frontend/imgs/{comparison_dir.name}/norm.jpg",
            f"frontend/imgs/{comparison_dir.name}/drag.jpg"
        ))

@webfrontend.route("/")
def main():
    """view method: landing page -- insert the gallery images and
    branding tagline"""
    return render_template(
        "frontend/main.html",
        gallery_imgs=GALLERY_IMGS,
        loadingLine="uploading lerk...",
        loadedLine=random.choice(RESULT_TAGS),
        branding_tagline=random.choice(BRANDING_TAGLINES),
    )