import os
from google.cloud import storage


storage_client = storage.Client()


def upload(fp, f_name, bucket):
    bucket = storage_client.get_bucket(bucket)
    blob = bucket.blob(f_name)
    blob.upload_from_filename(fp)

def download(fp, f_name, bucket):
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(f_name)
    blob.download_to_filename(fp)