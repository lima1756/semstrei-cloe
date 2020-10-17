import jwt
import datetime
from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    enabled = db.Column(db.Boolean, nullable=False, default=True)
    email = db.Column(db.String(128), index=True, unique=True)
    registered_on = db.Column(db.DateTime, nullable=False)
    password_hash = db.Column(db.String(256))

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = self.set_password(password)
        self.admin = admin
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
                app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(
                auth_token,
                app.config.get('SECRET_KEY'),
                algorithms=['HS256']
            )
            return payload['id']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False
