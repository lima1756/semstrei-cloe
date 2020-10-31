
import unittest
import json

from app import App
from ..base_test_app import BaseTestApp
from app.models.UserData import UserData
from app.models.RecoveryTokens import RecoveryTokens
from app.libs import db


class TestPasswordRecovery(BaseTestApp):

    def request_recover(self):
        res = self.client.get(
            'api/recover/request?email='+self.user_testing_email,
        )
        return res

    def test_request_recover_password(self):
        res = self.request_recover()
        self.assert_success(res)

    def test_recover_password(self):
        password_to_change = "changed"
        recovery_req_res = self.request_recover()
        # Verifying that recovery was send correctly
        self.assert_success(recovery_req_res)
        user1 = UserData.query.filter_by(email=self.user_testing_email).first()
        user1.set_password(password_to_change)
        self.db.session.add(user1)
        self.db.session.commit()
        user1 = UserData.query.filter_by(email=self.user_testing_email).first()
        # checking password to change was set
        self.assertTrue(user1.check_password(password_to_change))
        token = RecoveryTokens.query.first()
        res = self.client.put(
            'api/recover?token='+token.key,
            data=json.dumps({'password': self.password}),
            content_type='application/json'
        )
        user1 = UserData.query.filter_by(email=self.user_testing_email).first()
        # checking that request was succesful
        self.assert_success(res)
        # checking password set through request is set
        self.assertTrue(user1.check_password(self.password))
