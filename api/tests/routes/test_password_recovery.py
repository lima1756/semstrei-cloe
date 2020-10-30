
import unittest
import json

from app import App
from ..base import BaseTestCase
BaseTestCase.create_app()
from app.models.UserData import UserData
from app.models.RecoveryTokens import RecoveryTokens


app = App.get_instance().app
db = App.get_instance().db

class TestPasswordRecovery(BaseTestCase):

    user1_email = "user1@testingemail.com"
    password='password'

    @classmethod
    def setUpClass(cls):
        user1 = UserData(
            email=cls.user1_email,
            password=cls.password,
            name='name',
            phone_number='065156',
            admin=False,
            role=1
        )
        db.session.add(user1)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        user1 = UserData.query.filter_by(
            email=cls.user1_email
        ).first()
        db.session.query(RecoveryTokens).delete()
        db.session.delete(user1)
        db.session.commit()

    def request_recover(self):
        res = self.client.get(
            'api/recover/request?email='+self.user1_email,
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
        user1 = UserData.query.filter_by(email=self.user1_email).first()
        user1.set_password(password_to_change)
        db.session.add(user1)
        db.session.commit()
        user1 = UserData.query.filter_by(email=self.user1_email).first()
        # checking password to change was set
        self.assertTrue(user1.check_password(password_to_change))
        token = RecoveryTokens.query.first()
        res = self.client.put(
            'api/recover?token='+token.key,
            data=json.dumps({'password': self.password}),
            content_type='application/json'
        )
        user1 = UserData.query.filter_by(email=self.user1_email).first()
        # checking that request was succesful
        self.assert_success(res)
        # checking password set through request is set
        self.assertTrue(user1.check_password(self.password))