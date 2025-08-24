from flask import Flask
from flask_cors import CORS
from .config import Config
from .extensions import db, jwt
from .main import main_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize CORS
    CORS(app)

    # Initialize other extensions
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()

    return app
