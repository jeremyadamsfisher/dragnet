import os
from flask import Flask
from config import configs

app = Flask(__name__, instance_relative_config=True)
try:
    conf_setting = os.environ["DRAGNET_DEPLOYMENT"]
    config = configs[conf_setting]()
except KeyError:
    raise Exception("configuration not specified or specified"
                    "configuration does not exist!")
app.config.from_object(config)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = app.config["SECRETS_JSON_FP"]

# register blueprint
from .api import api
app.register_blueprint(api, url_prefix="/api")

from .frontend import webfrontend
app.register_blueprint(webfrontend, url_prefix="/app")

# make homepage the web frontend
from flask import redirect, url_for
app.route("/")(lambda: redirect(url_for("webfrontend.main")))