import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
app = Flask(__name__, instance_relative_config=True)
CORS(app)
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
app.config.from_object("config")
from app import views