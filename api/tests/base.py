import logging

from flask_testing import TestCase

from app import app, config, start
from app.config import TestingConfig as app_config

class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        config(app_config)
        start()
        from app import db
        db.create_all()
        return app