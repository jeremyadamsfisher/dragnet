import PIL
from PIL.Image import Image
from google.cloud import storage
from google.cloud import tasks_v2
from flask import current_app as app

def resize_image(img: Image, max_size=512) -> Image:
    """resize an image such that its major axis is
    no larger than specified
    """
    x, y = img.size
    major_axis = max((x, y))
    scale_factor = max_size / major_axis
    x_scaled = int(x * scale_factor)
    y_scaled = int(y * scale_factor)
    img.thumbnail((x_scaled, y_scaled), PIL.Image.ANTIALIAS)
    return img


def upload_gcp_bucket(fp, f_name, bucket):
    bucket = storage.Client().get_bucket(bucket)
    blob = bucket.blob(f_name)
    blob.upload_from_filename(fp)


def download_gcp_bucket(fp, f_name, bucket):
    bucket = storage.Client().bucket(bucket)
    blob = bucket.blob(f_name)
    blob.download_to_filename(fp)


def create_gcloud_task(method, relative_uri):
    client = tasks_v2.CloudTasksClient()
    parent = client.queue_path(
        app.config["GCLOUD_PROJECT_NAME"],
        app.config["GCLOUD_REGION"],
        app.config["GCLOUD_QUEUE_NAME"],
    )
    client.create_task(parent, {
        "app_engine_http_request": {
            "http_method": method,
            "relative_uri": relative_uri,
        }
    })