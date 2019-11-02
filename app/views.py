from flask import render_template
from app import app

@app.route('/')
def main_page():
    return render_template(
        "main.html"
    )