from flask import Flask, render_template
import logging
from logging import Formatter, FileHandler
from .extensions import db, migrate, moment
from .utils import format_datetime
from jinja2 import Environment, FileSystemLoader

def create_app():
    """
    Create and configure an instance of the Flask application.

    This function sets up the Flask app, including:
    - Configuration
    - Database initialization
    - Custom Jinja2 filters
    - Blueprint registration
    - Error handlers
    - Logging (in non-debug mode)

    Returns:
        Flask: The configured Flask application instance.
    """

    app = Flask(__name__)
    app.config.from_object('config')

    def startswith(string, prefix):
        """
        Custom Jinja2 filter to check if a string starts with a given prefix.

        Args:
            string (str): The string to check.
            prefix (str): The prefix to look for.

        Returns:
            bool: True if the string starts with the prefix, False otherwise.
        """
        if string is None:
            return False
        return string.startswith(prefix)

    env = Environment(loader=FileSystemLoader('templates'))
    env.filters['startswith'] = startswith

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    moment.init_app(app)

    # Register custom Jinja2 filters
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['startswith'] = startswith

    # Register blueprints
    from .blueprints.main import main_bp
    from .blueprints.venues import venues_bp
    from .blueprints.artists import artists_bp
    from .blueprints.shows import shows_bp
    from .blueprints.api import api_bp

    app.register_blueprint(main_bp, url_prefix='/home')
    app.register_blueprint(venues_bp, url_prefix='/venues')
    app.register_blueprint(artists_bp, url_prefix='/artists')
    app.register_blueprint(shows_bp, url_prefix='/shows')
    app.register_blueprint(api_bp, url_prefix='/api')

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        """Handle 404 errors by rendering a custom error page."""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        """Handle 500 errors by rendering a custom error page."""
        return render_template('errors/500.html'), 500

    # Configure logging for production mode
    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')

    return app
