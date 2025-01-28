
import logging

logging.basicConfig(level=logging.INFO)
logging.info("Initializing Flask app...")


from flask import Flask

from app.routes import api  # Import routes (blueprint)


def create_app():
    app = Flask(__name__)

    # Register the blueprint for routes
    app.register_blueprint(api)

    return app



