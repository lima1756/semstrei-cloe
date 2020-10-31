import logging
import json

from functools import wraps
from flask_testing import TestCase

from app import App
from app.config import TestingConfig as app_config
from app.models.UserData import UserData


class BaseTestApp(TestCase):
    """ Base Tests """

    admin_email = "admin@testingemail.com"
    user_status_email = "user1@testingemail.com"
    user_deletable_email = "user2@testingemail.com"
    user_testing_email = "user3@testingemail.com"
    user_name = "test name"
    user_phone_number = "331233112"
    password = 'password'

    def setUp(self):
        self.db = self.flask_app.db
        self.client = self.app.test_client()
        # if last run failed, there may be existing data so we tear down
        self.tearDown()
        with self.app.app_context():
            self.db.create_all()
            admin = UserData(
                email=self.admin_email,
                password=self.password,
                name=self.user_name,
                phone_number=self.user_phone_number,
                admin=True,
                role=0
            )
            user1 = UserData(
                email=self.user_status_email,
                password=self.password,
                name=self.user_name,
                phone_number=self.user_phone_number,
                admin=False,
                role=1
            )
            user2 = UserData(
                email=self.user_deletable_email,
                password=self.password,
                name=self.user_name,
                phone_number=self.user_phone_number,
                admin=False,
                role=1
            )
            user3 = UserData(
                email=self.user_testing_email,
                password=self.password,
                name=self.user_name,
                phone_number=self.user_phone_number,
                admin=False,
                role=1
            )
            self.db.session.add(user1)
            self.db.session.add(user2)
            self.db.session.add(user3)
            self.db.session.add(admin)
            self.db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def create_app(self):
        self.flask_app = App.get_instance(app_config)
        self.app = self.flask_app.app
        return self.app

    def assert_success(self, res, message=''):
        self.assertTrue(json.loads(res.data)[
                        'status'] == 'success', 'Request failed:'+message)
