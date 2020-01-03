import os
from flask import Flask
from .config import ProdConfig, LocalConfig

app = Flask(__name__, instance_relative_config=True)
is_local = os.environ.get("DRAGNET_LOCAL_DEPLOYMENT", False)
app.config.from_object(LocalConfig() if is_local else ProdConfig())

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config["SECRETS_JSON_FP"]

from app import views, backend