from flask import Blueprint
webfrontend = Blueprint(
    "webfrontend",
    __name__,
)
from .views import *