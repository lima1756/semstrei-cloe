import jwt
import string
import random
import datetime
import os
from dotenv import load_dotenv
from app.libs import db
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
JWT_KEY = 'JWT_KEY'


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(128), index=True, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    new_user = db.Column(db.Boolean, default=True)
    role = db.relationship('Role', backref='role', lazy=True)

    def __init__(self, email, password, name, phone_number, role, admin=False):
        self.email = email
        self.password = self.set_password(password)
        self.name = name
        self.phone_number = phone_number
        self.admin = admin
        self.role_id = role
        self.registered_on = datetime.datetime.now()
        self.enabled = True

    @staticmethod
    def gen_password(length=12):
        password_characters = string.ascii_letters + string.digits
        plain_password = ''.join(
            (random.choice(password_characters) for i in range(length)))
        return plain_password

    def __repr__(self):
        return '<UserData {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, session_days_duration=1, expiration_datetime=None):
        try:
            if expiration_datetime is None:
                expiration_datetime = datetime.datetime.utcnow(
                ) + datetime.timedelta(days=session_days_duration, seconds=0)
            payload = {
                'exp': expiration_datetime,
                'iat': datetime.datetime.utcnow(),
                'id': self.id
            }
            return jwt.encode(
                payload,
                os.getenv(JWT_KEY),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                os.getenv(JWT_KEY),
                algorithms=['HS256']
            )
            return payload['id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def get_payload_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                os.getenv(JWT_KEY),
                algorithms=['HS256']
            )
            return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def get_data_as_dict(self):
        return {
            'user_id': self.id,
            'email': self.email,
            'name': self.name,
            'phone_number': self.phone_number,
            'admin': self.admin,
            'enabled': self.enabled,
            'registration_date': self.registered_on,
            'role': self.role_id,
            'new_user': self.new_user
        }
