import logging

from flask_testing import TestCase

from app import app, db
from app.config import TestingConfig as app_config

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config)
        logging.basicConfig(
            level=app_config.LOGGING_LEVEL,
            format=app_config.LOGGING_FORMAT,
            filename=app_config.LOGGING_FILE
        )
        db.create_all()
        return app