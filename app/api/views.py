from . import api

import requests
import PIL
import tempfile
import io
import uuid

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
                    img = PIL.ImageOps.exif_transpose(img)
                    resized_img = utils.resize_image(img)
                except OSError:
                    abort(415)  # image that PIL cannot ingest
                resized_img.save(fp, "JPEG")
                utils.upload_gcp_bucket(fp, img_id, app.config["GCLOUD_INTERMEDIARY_BUCKET"])
            # run the machine learning task on a worker using gcloud tasks
            utils.create_gcloud_task("GET", url_for(".predict", img_id=img_id))
            j = {
                "result": url_for(".checkprogress", img_id=img_id),
                "img_id": img_id,
            }
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
        utils.download_gcp_bucket(fp_in, img_id, app.config["GCLOUD_INTERMEDIARY_BUCKET"])
        img = PIL.Image.open(fp_in).convert("RGB")
        img = translate(img)
        img.save(fp_out, format="JPEG")
        utils.upload_gcp_bucket(fp_out, img_id, app.config["GCLOUD_DRAG_BUCKET"])
        return "", 200


@api.route("/savetogallery/<img_id>")
def save_to_gallery(img_id: str):
    utils.copy_between_buckets(
        img_id,
        app.config["GCLOUD_DRAG_BUCKET"],
        app.config["GCLOUD_GALLERY_BUCKET"]
    )
    return "", 200