from app.libs import db


class OtbResults(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    numberCurrentPeriodOTB = db.Column(db.Integer, nullable=False, default=-1)
    daysLongCurrentPeriodOTB = db.Column(
        db.Integer, nullable=False, default=-1)
    startDateCurrentPeriodOTB = db.Column(db.DateTime, nullable=False)

    isFutureProjection = db.Column(db.Boolean, nullable=False, default=False)
    daysLongProjectionPeriodOTB = db.Column(
        db.Integer, nullable=False, default=-1)
    startDateProjectionPeriodOTB = db.Column(db.DateTime, nullable=True)

    une = db.Column(db.String(128), nullable=False)
    submarca = db.Column(db.String(128), nullable=False)
    categoria = db.Column(db.String(128), nullable=False)
    mercado = db.Column(db.String(128), nullable=False)

    initialStock = db.Column(db.Numeric(), nullable=False, default=0.0)
    inventoryOnStores = db.Column(db.Numeric(), nullable=False, default=0.0)
    purchases = db.Column(db.Numeric(), nullable=False, default=0.0)
    devolution = db.Column(db.Numeric(), nullable=False, default=0.0)
    targetSells = db.Column(db.Numeric(), nullable=False, default=0.0)
    targetStock = db.Column(db.Numeric(), nullable=False, default=0.0)
    projectionEomStock = db.Column(db.Numeric(), nullable=False, default=0.0)
    otb_minus_ctb = db.Column(db.Numeric(), nullable=False, default=0.0)
    percentage_otb = db.Column(db.Numeric(), nullable=False, default=0.0)

    def __init__(self, numberCurrentPeriodOTB, daysLongCurrentPeriodOTB, startDateCurrentPeriodOTB,
                 isFutureProjection, daysLongProjectionPeriodOTB, startDateProjectionPeriodOTB,
                 une, submarca, categoria, mercado, initialStock, inventoryOnStores,
                 purchases, devolution, targetSells, targetStock, projectionEomStock,
                 otb_minus_ctb, percentage_otb):
        self.numberCurrentPeriodOTB = numberCurrentPeriodOTB
        self.daysLongCurrentPeriodOTB = daysLongCurrentPeriodOTB
        self.startDateCurrentPeriodOTB = startDateCurrentPeriodOTB

        self.isFutureProjection = isFutureProjection
        self.daysLongProjectionPeriodOTB = daysLongProjectionPeriodOTB
        self.startDateProjectionPeriodOTB = startDateProjectionPeriodOTB

        self.une = une
        self.submarca = submarca
        self.categoria = categoria
        self.mercado = mercado

        self.initialStock = initialStock
        self.inventoryOnStores = inventoryOnStores
        self.purchases = purchases
        self.devolution = devolution
        self.targetSells = targetSells
        self.targetStock = targetStock
        self.projectionEomStock = projectionEomStock
        self.otb_minus_ctb = otb_minus_ctb
        self.percentage_otb = percentage_otb

    def __repr__(self):
        return '<OTB calculations of Date: {}, for Period: {}, Une:{}, Submarca:{}, Mercado:{}, Categoria:{}>'\
            .format(self.startDateCurrentPeriodOTB, self.startDateProjectionPeriodOTB, self.une, self.submarca,
                    self.mercado, self.categoria)
