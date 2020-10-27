import jwt
import datetime
from app import App
from werkzeug.security import generate_password_hash, check_password_hash

JWT_KEY = 'JWT_KEY'

app = App.get_instance().app
db = App.get_instance().db

class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(128), index=True, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    name = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(128), nullable=False)
    password_hash = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
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

    def __repr__(self):
        return '<UserData {}>'.format(self.email)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self, session_days_duration=1):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=session_days_duration, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'id': self.id
            }
            return jwt.encode(
                payload,
                app.config.get(JWT_KEY),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                app.config.get(JWT_KEY),
                algorithms=['HS256']
            )
            return payload['id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

