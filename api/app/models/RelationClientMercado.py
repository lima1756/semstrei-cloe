from app.libs import db


class RelationClientMercado(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    client = db.Column(db.String(128), nullable=False)
    isM1 = db.Column(db.Boolean, nullable=False, default=True)

    def __init__(self, client, is_m1):
        self.client = client
        self.isM1 = is_m1

    def __repr__(self):
        return 'Express if the Client:{} forms part of the M1 share.'.format(self.client)
