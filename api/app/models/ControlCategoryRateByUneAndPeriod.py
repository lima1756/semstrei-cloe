import jwt
import datetime
from app import App
from werkzeug.security import generate_password_hash, check_password_hash

JWT_KEY = 'JWT_KEY'

app = App.get_instance().app
db = App.get_instance().db


class OtbResults(db.Model):
    _id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    month = db.Column(db.String(128), nullable=False)
    une = db.Column(db.String(128), nullable=False)
    rate_category_moda = db.Column(db.Double, nullable=False, default=0.0)
    date = db.Column(db.Date, nullable=False)

    def __init__(self, month, une, rate_category_moda, date):
        self.month = month
        self.une = une
        self.date = date
        if 0 <= rate_category_moda <= 1:
            self.rate_category_moda = rate_category_moda
        else:
            raise Exeption("Rate Category Moda must be a value from 0 to 1 inclusive.")

    def __repr__(self):
        return '<Rate of Category: "moda" items to buy given the {} and une: {}>'.format(self.month, self.une)