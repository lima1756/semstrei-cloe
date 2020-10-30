
import unittest
import json

from app import App
from ..base import BaseTestCase
BaseTestCase.create_app()
from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken


app = App.get_instance().app
db = App.get_instance().db

class TestAuth(BaseTestCase):

    admin_email = "admin@testingemail.com"
    password='password'

    @classmethod
    def setUpClass(cls):
        admin = UserData(
            email=cls.admin_email,
            password=cls.password,
            name='name',
            phone_number='0000000',
            admin=True,
            role=0
        )
        db.session.add(admin)
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        admin = UserData.query.filter_by(
            email=cls.admin_email
        ).first()
        db.session.delete(admin)
        db.session.query(BlacklistToken).delete()
        db.session.commit()

    def login(self):
        return self.client.post(
            'api/auth/login',
            data=json.dumps({'email': self.admin_email, 'password': self.password}),
            content_type='application/json'
        )

    def test_login(self):
        res = self.login()
        self.assert_success(res)

    def test_logout(self):
        res = self.login()
        token = json.loads(res.data)['auth_token']
        self.client.post(
            'api/auth/logout',
            headers={'Authorization': 'Bearer '+token}
        )
        blacklist = BlacklistToken.query.filter_by(
            token=token
        ).first()
        self.assertTrue(not (blacklist is None))