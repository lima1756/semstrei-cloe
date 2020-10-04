import os

from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig' # TODO: For production we would want to use ProductionConfig instead of DevelopmentConfig
)
app.config.from_object(app_settings)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: create a middleware logger: 
#   Info: Log all requests, if logged in and ip address
#   Error: log all python errors

# Registrando rutas
from .routes.user_management import user_management_blueprint
app.register_blueprint(user_management_blueprint)

from app import models