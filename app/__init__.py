from flask import Flask, render_template
import logging
from logging import Formatter, FileHandler
from .extensions import db, migrate, moment
from .utils import format_datetime

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # Register Jinja2 filter
    app.jinja_env.filters['datetime'] = format_datetime

    # Register blueprints
    from .blueprints.main import main_bp
    from .blueprints.venues import venues_bp
    from .blueprints.artists import artists_bp
    from .blueprints.shows import shows_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(venues_bp)
    app.register_blueprint(artists_bp)
    app.register_blueprint(shows_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500

    # Logging setup
    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app





