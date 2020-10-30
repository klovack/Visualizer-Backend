"""
Entry point of the application
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS


db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()


def create_app(test_config=None):
    """ create and configure the flask app """
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config.
        app.config.from_pyfile('config.py', silent=False)
    else:
        # load test config
        app.config.from_mapping(test_config)

    db.init_app(app)
    marshmallow.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
