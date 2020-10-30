import logging
import json

from flask_testing import TestCase

from app import App
from app.config import TestingConfig as app_config

class BaseTestCase(TestCase):
    """ Base Tests """

    @classmethod
    def create_app(cls):
        app = App.get_instance(app_config)
        app.db.create_all()
        return app.app
    
    def assert_success(self, res, message=''):
        self.assertTrue(json.loads(res.data)[
                        'status'] == 'success', 'Request failed:'+message)