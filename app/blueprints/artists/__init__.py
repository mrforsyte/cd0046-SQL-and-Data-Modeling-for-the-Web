from flask import Blueprints

artists_bp = Blueprints('artists', __name__)

from . import routes 

