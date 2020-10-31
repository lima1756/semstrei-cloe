
import unittest
import json

from app import App
from ..base_test_app import BaseTestApp
from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken
from app.libs import db


class TestAuth(BaseTestApp):

    def login(self):
        return self.client.post(
            'api/auth/login',
            data=json.dumps({'email': self.admin_email,
                             'password': self.password}),
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
