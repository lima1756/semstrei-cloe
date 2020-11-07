import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from .libs.extentions import db
from .libs.extentions import migrate
from .libs.extentions import mail
# rutas
from .routes import user_blueprint, password_recovery_blueprint, auth_blueprint,\
    otb_blueprint, otb_filters_blueprint
# modelos
from app.models import BlacklistToken, ControlCategoryRateByUneAndPeriod,\
    OtbResults, RecoveryTokens, RelationClientMercado, Role, UserData


class App:

    instance = None

    def __init__(self, app_config):
        if App.instance is None:
            App.instance = self
            self.app = Flask(__name__)
            self.db = db
            self.migrate = migrate
            self.mail = mail

            CORS(self.app)
            self.app.config.from_object(app_config)

            self.db.init_app(self.app)
            self.migrate.init_app(self.app, self.db)
            self.mail.init_app(self.app)

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
                filename=logging_dir + logging_file if logging_file else None
            )

            # Registrando rutas
            url_prefix = '/api'
            self.app.register_blueprint(user_blueprint, url_prefix=url_prefix)
            self.app.register_blueprint(
                password_recovery_blueprint,
                url_prefix=url_prefix
            )
            self.app.register_blueprint(auth_blueprint, url_prefix=url_prefix)
            self.app.register_blueprint(otb_blueprint, url_prefix=url_prefix)
            self.app.register_blueprint(otb_filters_blueprint, url_prefix=url_prefix)
        else:
            raise Exception(
                'Singletons must be accessed through `get_instance()`.')

    @classmethod
    def get_instance(cls, app_config=None):
        if cls.instance is None:
            return App(app_config)
        return cls.instance
