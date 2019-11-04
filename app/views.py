import os
import tempfile
import io
import random
import base64
import PIL
from flask import render_template, redirect, url_for, request
from .translate import translate

from app import app

@app.route("/gallery")
def gallery():
    return "not implemented yet"


@app.route("/")
def about():
    return render_template("about.html")


@app.route("/app")
def app_page():
    return render_template("app.html")


@app.route("/result", methods = ["POST"])  
def result():
    if request.method == "POST":  
        f = request.files["file"]
        with tempfile.NamedTemporaryFile("wb") as f_temp:
            f.save(f_temp.name)
            f_temp.seek(0)

            # make smaller to keep the memory footprint low
            img = PIL.Image.open(f_temp.name)
            x, y = img.size
            major_axis = max((x, y))
            x_scaled = int((x / major_axis) * 512)
            y_scaled = int((y / major_axis) * 512)
            img.thumbnail((x_scaled, y_scaled), PIL.Image.ANTIALIAS)

            # run through face.evoLVE and cycleGAN
            img = translate(img)

            web_output = io.BytesIO()
            img.convert('RGBA').save(web_output, format='PNG')
            web_output.seek(0, 0)
            web_output_b64 = base64.b64encode(web_output.getvalue()).decode('ascii')
            
            tags = [
                "Tens! Tens across the board!",
                "America, she's stunning!",
                "Start your engines, and may the best woman win...",
                "She already done had herses",
            ]

            return render_template(
                "result.html",
                img=web_output_b64,
                tag=random.choice(tags)
            )