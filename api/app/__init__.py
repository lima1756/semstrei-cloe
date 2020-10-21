import os
import logging
from dotenv import load_dotenv
from flask_mail import Mail

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

load_dotenv()
app = Flask(__name__)

# TODO: For production we would want to use ProductionConfig instead of DevelopmentConfig
from app.config import DevelopmentConfig as app_config
app.config.from_object(app_config)
db = SQLAlchemy(app)
mail = Mail(app)
migrate = Migrate(app, db)

# Configuring logger
logging.basicConfig(
    level=app_config.LOGGING_LEVEL,
    format=app_config.LOGGING_FORMAT,
    filename=app_config.LOGGING_FILE
)
# configuring mail logger
app.extensions['mail'].debug = 0

# Registrando Middleware
from .middleware import event_logger

# Registrando rutas
from .routes.user_management import user_management_blueprint
app.register_blueprint(user_management_blueprint)

from app import models
