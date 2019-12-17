import os
import tempfile
import io
import random
import pathlib
import uuid
import PIL

from pathlib import Path
from google.cloud import storage, tasks_v2
from flask import render_template, redirect, url_for, request, make_response, jsonify

from .translate import translate
from .constants import BRANDING_TAGLINES, TAGS
from app import app

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.abspath("./secrets.json")
storage_client = storage.Client()
client = tasks_v2.CloudTasksClient()
parent = client.queue_path("dragnet", "us-east1", "dragnet-queue")  # todo: put this in an .env

GALLERY_IMGS = []
for comparison_dir in pathlib.Path("./app/static/imgs").glob("*"):
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


def fail(msg):
    """view method: convenience failure state -- display
    failure to user
    
    Arguments:
        msg: message to display
    """
    return render_template(
        "app_failure.html",
        message=msg
    )


@app.route("/enqueue", methods=["POST"])
def enqueue():
    """view method: upload the user profile image, enqueue
    to cloud tasks send back redirect information"""
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
            return make_response(jsonify({"result_page": f"/result/{img_id}"}), 200)


@app.route('/result/<img_id>')
def result(img_id: str):
    return render_template(
        "app_result.html",
        img_id=img_id,
        tag=random.choice(TAGS)
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