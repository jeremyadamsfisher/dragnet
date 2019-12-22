import os
import tempfile
import io
import random
import pathlib
import uuid
import PIL
import base64
import requests

from os import path
from pathlib import Path
from google.cloud import storage, tasks_v2
from flask import render_template, redirect, url_for, request, make_response, jsonify

from .translate import translate
from .constants import BRANDING_TAGLINES, TAGS
from app import app


storage_client = storage.Client()
client = tasks_v2.CloudTasksClient()
parent = client.queue_path(
    os.environ["GCLOUD_PROJECT_NAME"],
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
                img_id = str(uuid.uuid4())
                data_b64 = payload[len("data:image/jpeg;base64,"):]
                data = base64.b64decode(data_b64)
                with tempfile.TemporaryDirectory() as t_dir:
                    fp = path.join(t_dir, "in.jpg")
                    with open(fp, "wb") as f:
                        f.write(data)
                    upload(fp, img_id, os.environ["GCLOUD_INTERMEDIARY_BUCKET"])
                client.create_task(parent, {
                    "app_engine_http_request": {
                        "http_method": "GET",
                        "relative_uri": f"/predict/{img_id}",
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
    drag_bucket = os.environ["GCLOUD_DRAG_BUCKET"]
    r = requests.get(f"https://storage.googleapis.com/{drag_bucket}/{img_id}")
    resp = {"drag_status": "loading"} if r.status_code == 404 else {"drag_status": "done"}
    return make_response(jsonify(resp))


@app.route("/predict/<img_id>")
def predict(img_id: str):
    """predict what someone looks like in drag and upload it to gcp
    
    Arguments:
        img_id: how we will save the file to gcp, front-end also knows about
    """
    with tempfile.TemporaryDirectory() as t_dir:
        fp_in = path.join(t_dir, "in.jpg")
        fp_out = path.join(t_dir, "out.jpg")
        download(fp_in, img_id, os.environ["GCLOUD_INTERMEDIARY_BUCKET"])
        img = PIL.Image.open(fp_in).convert("RGB")
        img = translate(img)
        img.save(fp_out, format="JPEG")
        upload(fp_out, img_id, os.environ["GCLOUD_DRAG_BUCKET"])


def upload(fp, f_name, bucket):
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(f_name)
    blob.upload_from_filename(fp)

def download(fp, f_name, bucket):
    bucket = storage_client.bucket(os.environ["GCLOUD_INTERMEDIARY_BUCKET"])
    blob = bucket.blob(f_name)
    blob.download_to_filename(fp)
