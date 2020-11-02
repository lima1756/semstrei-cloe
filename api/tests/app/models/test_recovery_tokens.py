import unittest
from ..base_test_app import BaseTestApp
from app.models.RecoveryTokens import RecoveryTokens
from app.models.UserData import UserData


class TestRecoveryTokens(BaseTestApp):

    user = UserData(
        email='test@test.com',
        password='test',
        name="test name",
        phone_number="1234567",
        role=1
    )

    def gen_token(self):
        return RecoveryTokens(self.user)

    def test_generate_token(self):
        token = self.gen_token()
        # Checking for instance of string instead of bytes, because it is saved
        # as string
        self.assertTrue(isinstance(token.key, str))

    def test_validate_token(self):
        token = self.gen_token()
        self.assertTrue(isinstance(token.key, str))
        self.assertTrue(RecoveryTokens.validate_key(token.key) == self.user.id)