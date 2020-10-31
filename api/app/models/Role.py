import jwt
import datetime
from app.libs import db


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name
