import unittest
import json
import random

from app import App
from ..base_test_app import BaseTestApp
from app.models.UserData import UserData
from app.models.RecoveryTokens import RecoveryTokens
from app.libs import db


class TestUserManagement(BaseTestApp):

    token = None

    def login(self, email=None):
        if email is None:
            email = self.admin_email
        return self.client.post(
            'api/auth/login',
            data=json.dumps({'email': email, 'password': self.password}),
            content_type='application/json'
        )

    def get_token(self, email=None):
        if email is None:
            email = self.admin_email
        res = self.login(email)
        return json.loads(res.data)['auth_token']

    def get_admin_token(self):
        if self.token:
            return self.token
        self.token = self.get_token()
        return self.token

    def test_user_registration(self):
        token = self.get_admin_token()
        res = self.client.post(
            'api/user',
            data=json.dumps({
                'email': "testing_mail@testingmail.com",
                'password': self.password,
                'name': self.user_name,
                'phone_number': self.user_phone_number,
                'admin': False,
                'role': 1
            }),
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )
        self.assert_success(res)

    def switch_user_status(self, endpoint, email):
        token = self.get_admin_token()
        user = UserData.query.filter_by(
            email=email
        ).first()
        return self.client.put(
            'api/user/'+str(user.id)+'/' + endpoint,
            content_type='application/json',
            headers={'Authorization': 'Bearer '+token}
        )

    def test_user_disable(self):
        res = self.switch_user_status('disable', self.user_status_email)
        self.assert_success(res)

    def test_user_enable(self):
        res = self.switch_user_status('enable', self.user_status_email)
        self.assert_success(res)

    def test_get_user_data(self):
        token = self.get_admin_token()
        res = self.client.get(
            'api/user',
            headers={'Authorization': 'Bearer '+token}
        )
        self.assert_success(res)

    def test_get_all_users(self):
        token = self.get_admin_token()
        res = self.client.get(
            'api/user/all',
            headers={'Authorization': 'Bearer '+token}
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'success')
        self.assertTrue(len(data['data']) > 0, 'The list of users is empty')

    def test_no_token_cannot_call_required_token_route(self):
        res = self.client.get(
            'api/user/all',
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_normal_user_cannot_call_admin_routes(self):
        token = self.get_token(self.user_testing_email)
        res = self.client.get(
            'api/user/all',
            headers={'Authorization': 'Bearer '+token}
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_disabled_user_cannot_login(self):
        self.switch_user_status('disable', self.user_status_email)
        res = self.login(self.user_status_email)
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_disabled_user_cannot_use_token(self):
        self.switch_user_status('enable', self.user_status_email)
        token = self.get_token(self.user_status_email)
        self.switch_user_status('disable', self.user_status_email)
        res = self.client.get(
            'api/user/all',
            headers={'Authorization': 'Bearer '+token}
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_delete_user(self):
        token = self.get_admin_token()
        user = UserData.query.filter_by(
            email=self.user_deletable_email
        ).first()
        res = self.client.delete(
            'api/user/'+str(user.id),
            headers={'Authorization': 'Bearer '+token}
        )
        self.assert_success(res)

    def test_delete_multiple_users(self):
        token = self.get_admin_token()
        users_id = []
        total_created = random.randint(2, 10)
        with self.app.app_context():
            for i in range(total_created):
                user = UserData(
                    email=str(i)+self.user_deletable_email,
                    password=self.password,
                    name=self.user_name,
                    phone_number=self.user_phone_number,
                    admin=False,
                    role=1
                )
                self.db.session.add(user)
                self.db.session.commit()
                users_id.append(user.id)
        res = self.client.delete(
            'api/user',
            content_type='application/json',
            data=json.dumps({'users': users_id}),
            headers={'Authorization': 'Bearer '+token}
        )
        response = json.loads(res.data)
        self.assertTrue(
            response['status'] == 'success',
            'request failed'
        )
        self.assertTrue(
            response['deleted'] == total_created,
            'The total of deleted users is different from the requested'
        )
