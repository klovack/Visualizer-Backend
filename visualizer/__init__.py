"""
Entry point of the application
"""
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_redis import FlaskRedis
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate()
marshmallow = Marshmallow()
CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
oauth = OAuth()
oauth.register(
    name='google',
    server_metadata_url=CONF_URL,
    client_kwargs={
        'scope': 'openid email profile'
    }
)
redis_client = FlaskRedis()


def create_app(test_config=None):
    """ create and configure the flask app """
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)

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
    CORS(app, origins=app.config['ORIGINS'], supports_credentials=True)
    oauth.init_app(app)
    redis_client.init_app(app)

    from .routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
