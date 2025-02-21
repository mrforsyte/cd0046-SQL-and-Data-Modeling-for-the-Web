from flask import Blueprint, current_app, render_template
from jinja2 import TemplateNotFound
from . import main_bp




@main_bp.route('/')
def index():
    current_app.logger.info("Entering index route")
    try:
        current_app.logger.info("Attempting to render template")
        return render_template('pages/home.html')

    except TemplateNotFound:
        current_app.logger.error("Template 'pages/home.html' not found")
        return render_template('errors/404.html'), 404

    