import unittest

from app import app, db
from app.models import User
from app.routes.user_management import DisableAPI, EnableAPI, GetAllUsers, LoginAPI, LogoutAPI, RemoveUserAPI, RegisterAPI
from ..base import BaseTestCase

# TODO: All this tests
class TestUserModel(BaseTestCase):

    def setUpModule(self):
        self.admin = User(
            email='test_admin',
            password='password',
            admin=True
        )
        db.session.add(self.admin)
        db.session.commit()
        self.client = app.test_client()

    def test_login(self):
        self.client.post()

    def test_user_registration(self):
        pass

    def test_user_disable(self):
        pass

    def test_user_enable(self):
        pass

    def test_user_deletion(self):
        pass

    def test_get_user_data(self):
        pass

    def test_get_all_users(self):
        pass

    def tearDownModule(self):
        # TODO: remove database (?)
        pass
