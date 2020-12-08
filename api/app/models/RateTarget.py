import datetime
from app.libs import db


class RateTarget(db.Model):
    """
    Token Model for storing JWT tokens
    """

    id = db.Column(db.Integer, primary_key=True)
    rate = db.Column(db.Numeric(), nullable=False, default=0.0)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self):
        self.updated_at = datetime.datetime.now()

    def update(self, rate):
      self.rate = rate
      self.updated_at = datetime.datetime.now()

    def __repr__(self):
        return '<RateTarget: {}'.format(self.rate)
