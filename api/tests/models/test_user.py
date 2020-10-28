import unittest
from ..base import BaseTestCase
BaseTestCase.create_app()
from app.models.UserData import UserData


class TestUserModel(BaseTestCase):
    
    def test_encode_auth_token(self):
        user = UserData(
            email='test@test.com',
            password='test',
            name="test name",
            phone_number="1234567",
            role=1
        )
        auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = UserData(
            email='test@test.com',
            password='test',
            name="test name",
            phone_number="1234567",
            role=1
        )
        auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(UserData.decode_auth_token(
            auth_token.decode("utf-8")) == user.id)
