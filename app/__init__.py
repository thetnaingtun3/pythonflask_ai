from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object("config.Config")

    # Register routes
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
