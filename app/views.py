import os
import tempfile
import io
import random
import base64
import PIL
from flask import render_template, redirect, url_for, request
from .translate import translate

from app import app


branding_taglines = [
    "GAN i get an amen?",
    "drag up your machine learning",
    "born naked and the rest is GAN",
    "style transfer for drag queens"
]

original_render_template = render_template
def render_template_(*args, **kwargs):
    return original_render_template(
        *args,
        **kwargs,
        branding_tagline=random.choice(branding_taglines)
    )
render_template = render_template_

@app.route("/gallery")
def gallery():
    return "not implemented yet"


@app.route("/")
def about():
    return render_template("about.html")


@app.route("/app")
def app_page():
    return render_template("app_input.html")


def fail(msg):
    return render_template("app_failure.html", message=msg)


@app.route("/result", methods=["POST"])
def result():
    if request.method == "POST":
        f = request.files["file"]

        if "heic" in f.filename.lower():
            return fail(f"could not translate {f.filename}")

        with tempfile.NamedTemporaryFile("wb+") as f_temp:
            f.save(f_temp.name)
            f_temp.seek(0)

            try:
                img = PIL.Image.open(f_temp.name)
            except OSError:
                return fail("could not process image!")

            img = img.convert("RGB")

            # # run through face.evoLVE and cycleGAN
            try:
                img = translate(img)
            except ValueError:
                return fail("no faces found!")

            web_output = io.BytesIO()
            img.save(web_output, format="PNG")
            web_output.seek(0, 0)
            web_output_b64 = base64.b64encode(web_output.getvalue()).decode("ascii")

            tags = [
                "Tens! Tens across the board!",
                "America, she's stunning!",
            ]

            return render_template(
                "app_result.html", img=web_output_b64, tag=random.choice(tags)
            )
