import os

class BaseConfig:
    IS_LOCAL = os.environ.get("DRAGNET_LOCAL_DEPLOYMENT", False)  # production by default

    GCLOUD_DRAG_BUCKET          = "dragnet_imgs"
    GCLOUD_PROJECT_NAME         = "dragnet"
    GCLOUD_REGION               = "us-east1"
    GCLOUD_QUEUE_NAME           = "dragnet-queue"
    GCLOUD_INTERMEDIARY_BUCKET  = "dragnet_raw_imgs"

    SECRETS_JSON_FP     = "./secrets.json"

class LocalConfig(BaseConfig):
    DEBUG = True

class ProdConfig(BaseConfig):
    DEBUG = False


