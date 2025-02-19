
from werkzeug.serving import run_simple
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from forms import *
from datetime import datetime
from models import Venue, Artist, Show, Availability
from extensions import db, migrate
# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#
def create_app():
    app = Flask(__name__)
    moment = Moment(app)
    app.config.from_object('config')
    migrate = Migrate(app, db)

    app.jinja_env.filters['datetime'] = format_datetime


    @app.route('/')
    def index():
        return render_template('pages/home.html')


    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404


    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')






