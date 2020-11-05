from flask import Blueprint, request, make_response, render_template
from flask.views import MethodView
from sqlalchemy.sql import func
from app.models.OtbResults import OtbResults
from app.libs import db
import random
import time
import string
import simplejson

otb_blueprint = Blueprint('otb', __name__)


class OTB(MethodView):
    def random_date(self, prop):
        format = '%d-%b-%Y'
        start = "01-JAN-2020"
        end = "01-DEC-2020"
        stime = time.mktime(time.strptime(start, format))
        etime = time.mktime(time.strptime(end, format))

        ptime = stime + prop * (etime - stime)

        return time.strftime(format, time.localtime(ptime))

    def gen_fake_data(self):
        letters = string.ascii_lowercase
        otb = []
        for i in range(150000):
            a = OtbResults(1, 30,
                           self.random_date(random.random()),
                           False, -1, self.random_date(random.random()),
                           random.choice(letters),
                           random.choice(letters),
                           random.choice(letters),
                           random.choice(letters),
                           random.randint(0, 50000),
                           random.randint(0, 50000),
                           random.randint(0, 50000),
                           random.randint(0, 500),
                           random.randint(0, 50000),
                           random.randint(0, 50000),
                           random.randint(0, 50000),
                           random.randint(0, 50000),
                           random.random()
                           )
            otb.append(a)
        db.session.bulk_save_objects(otb)
        db.session.commit()
        responseObject = {
            'status': 'success'
        }
        return make_response(simplejson.dumps(responseObject)), 200

    def post(self):
        # TODO: remove this
        return self.gen_fake_data()

    def get(self):
        categoria = request.args.get('categoria')
        une = request.args.get('une')
        submarca = request.args.get('submarca')
        mercado = request.args.get('mercado')
        current_period = request.args.get('current_period')

        # SELECT columns
        query = db.session.query(
            OtbResults.startDateCurrentPeriodOTB,
            OtbResults.startDateProjectionPeriodOTB,
            func.sum(OtbResults.initialStock).label('initialStock'),
            func.sum(OtbResults.inventoryOnStores).label('inventoryOnStores'),
            func.sum(OtbResults.purchases).label('purchases'),
            func.sum(OtbResults.devolution).label('devolution'),
            func.sum(OtbResults.targetSells).label('targetSells'),
            func.sum(OtbResults.targetStock).label('targetStock'),
            func.sum(OtbResults.projectionEomStock).label(
                'projectionEomStock'),
            func.sum(OtbResults.otb_minus_ctb).label('otb_minus_ctb'),
            func.sum(OtbResults.percentage_otb).label('percentage_otb'),
        )
        # WHERE
        filters = [
            # OtbResults.isFutureProjection == False,
            OtbResults.startDateCurrentPeriodOTB == current_period
        ]
        if categoria is not None:
            filters.append(OtbResults.categoria == categoria)
        if une is not None:
            filters.append(OtbResults.une == une)
        if submarca is not None:
            filters.append(OtbResults.submarca == submarca)
        if mercado is not None:
            filters.append(OtbResults.mercado == mercado)

        # GROUP BY
        group_by = [OtbResults.startDateProjectionPeriodOTB,
                    OtbResults.startDateCurrentPeriodOTB]

        res_query = query.filter(*filters).group_by(*group_by).all()
        response = []
        for row in res_query:
            response.append({
                "startDateCurrentPeriodOTB": row[0].isoformat(),
                "startDateProjectionPeriodOTB": row[1].isoformat(),
                "initialStock": row[2],
                "inventoryOnStores": row[3],
                "purchases": row[4],
                "devolution": row[5],
                "targetSells": row[6],
                "targetStock": row[7],
                "projectionEomStock": row[8],
                "otb_minus_ctb": row[9],
                "percentage_otb": row[10],
            })
        responseObject = {
            'status': 'success',
            'data': response
        }
        return make_response(simplejson.dumps(responseObject)), 200


otb_view = OTB.as_view('otb')
otb_blueprint.add_url_rule(
    '/otb',
    view_func=otb_view,
    methods=['GET', 'POST']
)
