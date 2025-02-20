from flask import Blueprint

artists_bp = Blueprint('artists', __name__)

from . import routes 

