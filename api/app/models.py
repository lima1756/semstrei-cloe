import jwt
from werkzeug.security import generate_password_hash, check_password_hash

class User():# db.Model):
    id = 0#db.Column(db.Integer, primary_key=True)
    admin = False
    email = ""#db.Column(db.String(120), index=True, unique=True)
    password_hash = ""#db.Column(db.String(128))

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = self.set_password(password)
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def __repr__(self):
        return '<User {}>'.format(self.email)    

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def encode_auth_token(self):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': self.id
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
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
