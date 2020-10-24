import os
import logging
from dotenv import load_dotenv
from flask_mail import Mail

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.config import DevelopmentConfig as development_config

load_dotenv()

class App:

    instance = None

    def __init__(self, app_config):
        if App.instance is None:
            App.instance = self
            self.app = Flask(__name__)
            if app_config is None:
                app_config = development_config
            self.app.config.from_object(app_config)
            self.db = SQLAlchemy(self.app)
            self.migrate = Migrate(self.app, self.db)
            self.mail = Mail(self.app)
            # configuring mail logger
            self.app.extensions['mail'].debug = 0
            # Configuring logger
            logging_dir = self.app.config.get('LOGGING_DIR')
            if not os.path.exists(logging_dir):
                os.makedirs(logging_dir)
            logging_file = self.app.config.get('LOGGING_FILE')
            logging.basicConfig(
                level=self.app.config.get('LOGGING_LEVEL'),
                format=self.app.config.get('LOGGING_FORMAT'),
                filename= logging_dir + logging_file if logging_file else None
            )

            # Registrando Middleware
            from .middleware import event_logger

            # Registrando rutas
            from .routes.user_management import user_management_blueprint
            url_prefix = '/api'
            self.app.register_blueprint(
                user_management_blueprint, 
                url_prefix=url_prefix
            )
            # Registrando modelos
            from . import models
        else:
            raise Exception('Singletons must be accessed through `get_instance()`.')

    @classmethod
    def get_instance(cls, app_config = None):
        if cls.instance is None:
            return App(app_config)
        return cls.instance
