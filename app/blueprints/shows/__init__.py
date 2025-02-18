from flask import Blueprint

shows_bp = Blueprint('shows',__name__)

from .import routes

