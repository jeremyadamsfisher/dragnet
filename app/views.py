import os
import tempfile
from flask import render_template, redirect, url_for, request
from app import app


@app.route("/")
def main_page():
    return render_template("main.html")


@app.route('/upload', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']
        with tempfile.NamedTemporaryFile() as f_temp:
            f.save(f_temp.name)
            return render_template("success.html", name = f_temp.name)