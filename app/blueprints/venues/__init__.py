""" This module initializes blueprint for venues"""

from flask import Blueprint
venues_bp = Blueprint('venues', __name__)
from . import routes 