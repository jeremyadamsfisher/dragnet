from flask import Blueprint
api = Blueprint(
    "api",
    __name__,
)

import requests
import PIL
import tempfile
import io
import uuid

from google.cloud import tasks_v2
from os import path
from flask import (
    url_for,
    request,
    make_response,
    jsonify,
    abort,
    current_app as app
)

from . import utils
from .storage import download, upload
from .machine_learning import translate

@api.route("/enqueue", methods=["POST"])
def enqueue():
    """view method: upload the user profile image, enqueue
    to cloud tasks send back redirect information"""
    if request.method == "POST":
        payload = request.get_data()
        if not payload:
            abort(400)  # bad request
        else:
            img_id = str(uuid.uuid4())
            with tempfile.TemporaryDirectory() as t_dir:
                fp = path.join(t_dir, "in.jpg")
                try:
                    img = PIL.Image.open(io.BytesIO(payload)).convert("RGB")
                    resized_img = utils.resize_image(img)
                except OSError:
                    abort(415)
                resized_img.save(fp, "JPEG")
                upload(fp, img_id, app.config["GCLOUD_INTERMEDIARY_BUCKET"])
            client = tasks_v2.CloudTasksClient()
            parent = client.queue_path(
                app.config["GCLOUD_PROJECT_NAME"],
                app.config["GCLOUD_REGION"],
                app.config["GCLOUD_QUEUE_NAME"],
            )
            client.create_task(parent, {
                "app_engine_http_request": {
                    "http_method": "GET",
                    "relative_uri": url_for(".predict", img_id=img_id),
                }
            })
            j = {"result": url_for(".checkprogress", img_id=img_id)}
            return make_response(jsonify(j), 200)


@api.route("/checkprogress/<img_id>")
def checkprogress(img_id: str):
    """ping cloud tasks to see if the image is cooked"""
    drag_bucket = app.config["GCLOUD_DRAG_BUCKET"]
    url = f"https://storage.googleapis.com/{drag_bucket}/{img_id}"
    r = requests.get(url)
    if r.status_code == 404:
        return make_response(jsonify({"status": "loading"}))
    else:
        return make_response(jsonify({"status": "done", "url": url}))


@api.route("/predict/<img_id>")
def predict(img_id: str):
    """predict what someone looks like in drag and upload it to gcp
    
    Arguments:
        img_id: how we will save the file to gcp, front-end also knows about
    """
    with tempfile.TemporaryDirectory() as t_dir:
        fp_in = path.join(t_dir, "in.jpg")
        fp_out = path.join(t_dir, "out.jpg")
        download(fp_in, img_id, app.config["GCLOUD_INTERMEDIARY_BUCKET"])
        img = PIL.Image.open(fp_in).convert("RGB")
        img = translate(img)
        img.save(fp_out, format="JPEG")
        upload(fp_out, img_id, app.config["GCLOUD_DRAG_BUCKET"])