from flask import Flask
from .extensions import db, migrate, moment
from .utils import format_datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    app.jinja_env.filters['datetime'] = format_datetime

    from .blueprints.main import main_bp
    from .blueprints.venues import venues_bp
    from .blueprints.artists import artists_bp
    from .blueprints.shows import shows_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(venues_bp)
    app.register_blueprint(artists_bp)
    app.register_blueprint(shows_bp)

    return app