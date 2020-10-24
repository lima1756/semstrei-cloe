import os
import logging
from dotenv import load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import DevelopmentConfig as app_config

load_dotenv()

app = Flask(__name__)
db = None
migrate = None
models = None
config_run = False

def config(app_config):
    app.config.from_object(app_config)
    config_run = True

def start():
    global db
    global migrate
    if not config_run:
        config(app_config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)

    # Configuring logger
    logging.basicConfig(
        level=app.config.get('LOGGING_LEVEL'),
        format=app.config.get('LOGGING_FORMAT'),
        filename=app.config.get('LOGGING_FILE')
    )

    # Registrando Middleware
    from .middleware import event_logger

    # Registrando rutas
    from .routes.user_management import user_management_blueprint
    app.register_blueprint(user_management_blueprint)
    # Registrando modelos
    from . import models
