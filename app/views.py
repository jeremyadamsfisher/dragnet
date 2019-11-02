import os
import tempfile
import io
import base64
import PIL
from flask import render_template, redirect, url_for, request
from .translate import translate

from app import app


@app.route("/")
def main_page():
    return render_template("main.html")

@app.route("/gallery")
def gallery():
    return "not implemented yet"

@app.route('/upload', methods = ['POST'])  
def success():
    if request.method == 'POST':  
        f = request.files['file']
        with tempfile.NamedTemporaryFile("wb") as f_temp:
            f.save(f_temp.name); f_temp.seek(0)
            img = translate(PIL.Image.open(f_temp.name))
            web_output = io.BytesIO()
            img.convert('RGBA').save(web_output, format='PNG')
            web_output.seek(0, 0)
            web_output_b64 = base64.b64encode(web_output.getvalue()).decode('ascii')
            return render_template("success.html", img=web_output_b64)

