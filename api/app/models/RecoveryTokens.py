import jwt
import os
import datetime
from dotenv import load_dotenv
from app import App

load_dotenv()
JWT_KEY = 'JWT_KEY'
db = App.get_instance().db


class RecoveryTokens(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(598))
    request_date = db.Column(db.DateTime, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, user):
        self.request_date = datetime.datetime.utcnow()
        self.expiration = self.request_date + datetime.timedelta(days=1)
        payload = {
            'exp': self.expiration,
            'iat': datetime.datetime.utcnow(),
            'id': user.id
        }
        self.key = jwt.encode(
            payload,
            os.getenv(JWT_KEY),
            algorithm='HS256'
        ).decode() # This decode is so the binary jwt is processed as string so the DB doesn't try to decode it itself
    
    @staticmethod
    def validate_key(key):
        payload = jwt.decode(
            key,
            os.getenv(JWT_KEY),
            algorithms=['HS256']
        )
        return payload['id']
