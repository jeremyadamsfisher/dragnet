import os
import tempfile
import io
import random
import pathlib
import uuid
import PIL
import base64

from pathlib import Path
from google.cloud import storage, tasks_v2
from flask import render_template, redirect, url_for, request, make_response, jsonify

from .translate import translate
from .constants import BRANDING_TAGLINES, TAGS
from app import app


storage_client = storage.Client()
client = tasks_v2.CloudTasksClient()
parent = client.queue_path(
    os.environ["GCLOUD_DRAG_BUCKET"],
    os.environ["GCLOUD_REGION"],
    os.environ["GCLOUD_QUEUE_NAME"],
)

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
        payload = request.get_data()
        try:
            if not payload:
                raise FileNotFoundError
            else:
                data_b64 = payload[len("data:image/jpeg;base64,"):]
                data = base64.b64decode(data_b64)
                img_id = str(uuid.uuid4())
                client.create_task(parent, {
                    "app_engine_http_request": {
                        "http_method": "POST",
                        "relative_uri": f"/predict/{img_id}",
                        "body": data,
                    }
                })
                return make_response(jsonify({"result": "success",
                                              "result_page": f"/result/{img_id}"}), 200)
        except FileNotFoundError:
            return make_response(jsonify({"result": "failure",
                                          "result_page": None}), 200)


@app.route("/result/<img_id>")
def result(img_id: str):
    """render the result"""
    return render_template(
        "app_result.html",
        img_id=img_id,
        tag=random.choice(TAGS)
    )


@app.route("/checkprogress/<img_id>")
def checkprogress(img_id: str):
    """ping cloud tasks to see if the image is cooked"""
    url = f"https://storage.googleapis.com/{os.environ['GCLOUD_DRAG_BUCKET']}/{img_id}"
    resp = {"status": "working"}
    return make_response(jsonify(resp), 200)


@app.route("/predict/<img_id>", methods=["POST"])
def predict(img_id: str):
    """predict what someone looks like in drag and upload it to gcp
    
    Arguments:
        img_id: how we will save the file to gcp, front-end also knows about
    """
    if request.method == "POST":
        payload = request.get_data()
        predict_(payload, img_id)


def predict_(payload: bytes, img_id:str):
    with tempfile.NamedTemporaryFile() as tf:
        img = PIL.Image.open(io.BytesIO(payload)).convert("RGB")
        img = translate(img)
        img.save(tf.name, format="PNG")
        bucket = storage_client.get_bucket(os.environ["GCLOUD_DRAG_BUCKET"])
        blob = bucket.blob(img_id)
        blob.upload_from_filename(tf.name)