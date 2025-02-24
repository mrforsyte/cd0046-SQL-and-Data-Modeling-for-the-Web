from app import create_app
import os

""" This script is the entry point for running the Flask application. It sets up the port
    and host for the development server and runs the app in debug mode.
"""

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 63653))
    app = create_app()
    app.run(host='0.0.0.0', port=port, debug=True)