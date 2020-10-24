import os
import logging
from dotenv import load_dotenv
from flask_mail import Mail

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import DevelopmentConfig as app_config

load_dotenv()

app = Flask(__name__)
db = None
migrate = None
models = None
mail = None
config_run = False

def config(app_config):
    app.config.from_object(app_config)
    config_run = True

def start():
    global db
    global migrate
    global mail
    if not config_run:
        config(app_config)
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    mail = Mail(app)
    # configuring mail logger
    app.extensions['mail'].debug = 0
    # Configuring logger
    logging_dir = app.config.get('LOGGING_DIR')
    if not os.path.exists(logging_dir):
        os.makedirs(logging_dir)
    logging_file = app.config.get('LOGGING_FILE')
    logging.basicConfig(
        level=app.config.get('LOGGING_LEVEL'),
        format=app.config.get('LOGGING_FORMAT'),
        filename= logging_dir + logging_file if logging_file else None
    )

    # Registrando Middleware
    from .middleware import event_logger

    # Registrando rutas
    from .routes.user_management import user_management_blueprint
    url_prefix = '/api'
    app.register_blueprint(user_management_blueprint, url_prefix=url_prefix)
    # Registrando modelos
    from . import models
