import os
import tempfile
import io
import random
import pathlib
import PIL
import uuid

from pathlib import Path
from threading import Thread
from google.cloud import storage, tasks_v2
from flask import render_template, redirect, url_for, request
from .translate import translate

from app import app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("./secrets.json")
storage_client = storage.Client()
client = tasks_v2.CloudTasksClient()
parent = client.queue_path("dragnet", "us-east1", "dragnet-queue")

branding_taglines = [
    "GAN i get an amen?",
    "drag up your machine learning",
    "born naked and the rest is GAN",
    "style transfer for drag queens"
]
tags = [
    "Tens! Tens across the board!",
    "America, shes stunning!",
]


gallery_imgs = []
for comparison_dir in pathlib.Path("./app/static/imgs").glob("*"):
    if not comparison_dir.is_dir():
        continue
    else:
        gallery_imgs.append((f"imgs/{comparison_dir.name}/norm.jpg", f"imgs/{comparison_dir.name}/drag.jpg"))


original_render_template = render_template
def render_template_(*args, **kwargs):
    """wrapper for flask render template that fills in the branding"""
    return original_render_template(
        *args,
        **kwargs,
        branding_tagline=random.choice(branding_taglines),
        gallery_imgs=gallery_imgs
    )
render_template = render_template_


@app.route("/")
def main():
    """landing page"""
    return render_template("main.html")


def fail(msg):
    """convenience failure state"""
    return render_template("app_failure.html", message=msg)


@app.route("/result", methods=["POST"])
def result():
    """result page; enqueue the prediction"""
    if request.method == "POST":
        
        profile_img = request.files["file"]

        if "heic" in profile_img.filename.lower():
            return fail(f"could not translate {profile_img.filename}")
        else:
            img_id = f"{uuid.uuid4()}.png"
            task = {
                "app_engine_http_request": {
                    "http_method": "POST",
                    "relative_uri": f"/predict/{img_id}",
                    "body": profile_img.read(),
                }
            }
            client.create_task(parent, task)

            return render_template(
                "app_result.html",
                img_id=img_id,
                tag=random.choice(tags)
            )


@app.route('/predict/<img_id>', methods=['POST'])
def predict(img_id: str):
    """predict what someone looks like in drag and upload it to gcp
    
    Arguments:
        img_id: how we will save the file to gcp, front-end also knows about
    """
    with tempfile.NamedTemporaryFile() as tf:
        if request.method == "POST":
            payload = request.get_data()
            img = PIL.Image.open(io.BytesIO(payload)).convert("RGB")
            img = translate(img)
            img.save(tf.name, format="PNG")
            bucket = storage_client.get_bucket(os.environ["GCLOUD_DRAG_BUCKET"])
            blob = bucket.blob(img_id)
            blob.upload_from_filename(tf.name)