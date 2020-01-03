from flask import Blueprint
webfrontend = Blueprint(
    "frontend",
    __name__,
    template_folder="templates",
    static_folder="static"
)
from .views import *