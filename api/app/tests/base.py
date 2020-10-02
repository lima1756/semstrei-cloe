from flask_testing import TestCase

# TODO: relative imports problem (?)
from app import app


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app.config.from_object('project.server.config.TestingConfig')
        return app