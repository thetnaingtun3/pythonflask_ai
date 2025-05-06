from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Load configurations
    app.config.from_object("config.Config")

    # Initialize database
    db.init_app(app)

    # Automatically create database tables
    with app.app_context():
        db.create_all()

    # Register routes
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    return app
