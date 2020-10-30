import unittest
import json

from app import App
from ..base import BaseTestCase
BaseTestCase.create_app()
from app.models.UserData import UserData
from app.models.RecoveryTokens import RecoveryTokens


app = App.get_instance().app
db = App.get_instance().db

class TestUserManagement(BaseTestCase):

    admin_email = "admin@testingemail.com"
    user1_email = "user1@testingemail.com"
    user2_email = "user2@testingemail.com"
    user3_email = "user3@testingemail.com"
    user_name = "test name"
    user_phone_number = "331233112"
    password = "password"
    client = app.test_client()
    token = None

    @classmethod
    def setUpClass(cls):
        admin = UserData(
            email=cls.admin_email,
            password=cls.password,
            name=cls.user_name,
            phone_number=cls.user_phone_number,
            admin=True,
            role=0
        )
        user1 = UserData(
            email=cls.user1_email,
            password=cls.password,
            name=cls.user_name,
            phone_number=cls.user_phone_number,
            admin=False,
            role=1
        )
        user2 = UserData(
            email=cls.user2_email,
            password=cls.password,
            name=cls.user_name,
            phone_number=cls.user_phone_number,
            admin=False,
            role=1
        )
        db.session.add(admin)
        db.session.add(user1)
        db.session.add(user2)
        db.session.query(RecoveryTokens).delete()
        db.session.commit()

    @classmethod
    def tearDownClass(cls):
        admin = UserData.query.filter_by(
            email=cls.admin_email
        ).first()
        user1 = UserData.query.filter_by(
            email=cls.user1_email
        ).first()
        user2 = UserData.query.filter_by(
            email=cls.user2_email
        ).first()
        user3 = UserData.query.filter_by(
            email=cls.user3_email
        ).first()
        db.session.delete(admin)
        if(user1):
            db.session.delete(user1)
        if(user2):
            db.session.delete(user2)
        if(user3):
            db.session.delete(user3)
        db.session.commit()

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
                'email': self.user3_email,
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
        res = self.switch_user_status('disable', self.user1_email)
        self.assert_success(res)

    def test_user_enable(self):
        res = self.switch_user_status('disable', self.user1_email)
        self.assert_success(res)

    def test_user_deletion(self):
        res = self.switch_user_status('disable', self.user2_email)
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
        self.switch_user_status('enable', self.user1_email)
        token = self.get_token(self.user1_email)
        res = self.client.get(
            'api/user/all',
            headers={'Authorization': 'Bearer '+token}
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_disabled_user_cannot_login(self):
        self.switch_user_status('disable', self.user1_email)
        res = self.login(self.user1_email)
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')

    def test_disabled_user_cannot_use_toke(self):
        self.switch_user_status('enable', self.user1_email)
        token = self.get_token(self.user1_email)
        self.switch_user_status('disable', self.user1_email)
        res = self.client.get(
            'api/user/all',
            headers={'Authorization': 'Bearer '+token}
        )
        data = json.loads(res.data)
        self.assertTrue(data['status'] == 'fail')
