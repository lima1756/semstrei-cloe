import logging

from flask_testing import TestCase

from app import app, db
from app.config import TestingConfig as app_config

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object(app_config)
        db.create_all()
        return app