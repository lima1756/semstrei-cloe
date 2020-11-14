from flask import Blueprint, request, make_response, render_template
from sqlalchemy import asc
from sqlalchemy.sql import func
from app.models.OtbResults import OtbResults
from app.libs import db
from app.libs.decorators import login_required
from app.libs import validation
from .route_view import RouteView
import simplejson
# import random
# import time
# import string

otb_blueprint = Blueprint('otb', __name__)


class OTB(RouteView):
    # def random_date(self, prop):
    #     format = '%d-%b-%Y'
    #     start = "01-JAN-2020"
    #     end = "01-DEC-2020"
    #     stime = time.mktime(time.strptime(start, format))
    #     etime = time.mktime(time.strptime(end, format))

    #     ptime = stime + prop * (etime - stime)

    #     return time.strftime(format, time.localtime(ptime))

    # def gen_fake_data(self):
    #     letters = string.ascii_lowercase
    #     otb = []
    #     for i in range(150000):
    #         a = OtbResults(1, 30,
    #                        self.random_date(random.random()),
    #                        False, -1, self.random_date(random.random()),
    #                        random.choice(letters),
    #                        random.choice(letters),
    #                        random.choice(letters),
    #                        random.choice(letters),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 500),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 50000),
    #                        random.randint(0, 50000),
    #                        random.random()
    #                        )
    #         otb.append(a)
    #     db.session.bulk_save_objects(otb)
    #     db.session.commit()
    #     responseObject = {
    #         'status': 'success'
    #     }
    #     return make_response(simplejson.dumps(responseObject)), 200

    # def post(self):
    #     return self.gen_fake_data()

    def get_table(self, categoria, submarca, une, mercado, current_period, breakdown=False):

        # SELECT columns
        select = [
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
        ]

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
        group_by = [
            OtbResults.startDateProjectionPeriodOTB,
            OtbResults.startDateCurrentPeriodOTB
        ]

        # ORDER BY
        order_by = []

        if breakdown:
            select.extend(
                [OtbResults.categoria,
                 OtbResults.submarca,
                 OtbResults.une,
                 OtbResults.mercado]
            )
            group_by.extend(
                [OtbResults.categoria,
                 OtbResults.submarca,
                 OtbResults.une,
                 OtbResults.mercado]
            )
            order_by.extend(
                [OtbResults.categoria,
                 OtbResults.submarca,
                 OtbResults.une,
                 OtbResults.mercado]
            )

        order_by.append(asc(OtbResults.startDateProjectionPeriodOTB))

        res_query = db.session.query(*select)\
            .filter(*filters).group_by(*group_by)\
            .order_by(*order_by).all()
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
                "categoria": row[11] if len(row) > 11 else categoria,
                "submarca": row[12] if len(row) > 12 else submarca,
                "une": row[13] if len(row) > 13 else une,
                "mercado": row[14] if len(row) > 14 else mercado,
            })
        return response

    @login_required
    def get(self):
        try:
            check = validation.InputValidation({
                'categoria': request.args.get('categoria'),
                'une': request.args.get('une'),
                'submarca': request.args.get('submarca'),
                'mercado': request.args.get('mercado'),
                'current_period': request.args.get('current_period'),
            }, {
                'categoria': [validation.Strip, validation.ValidateAlphabeticString],
                'une': [validation.Strip, validation.ValidateAlphabeticString],
                'submarca': [validation.Strip, validation.ValidateAlphabeticString],
                'mercado': [validation.Strip, validation.ValidateAlphabeticString],
                'current_period': [validation.Strip, validation.ValidateDate],
            })
            data = check.validate()
        except validation.DataNotValidException:
            return self.return_data_not_valid(check)
        breakdown = request.args.get('breakdown') == 'True'
        table = self.get_table(data['categoria'], data['submarca'], data['une'],
                               data['mercado'], data['current_period'])
        breakdown_tables = None
        if breakdown:
            breakdown_tables = []
            curr_table = -1
            breakdown_res = self.get_table(data['categoria'], data['submarca'], data['une'],
                                           data['mercado'], data['current_period'], True)
            for i in range(len(breakdown_res)):
                if i != 0:
                    last = breakdown_res[i-1]
                    curr = breakdown_res[i]
                    if not (last['categoria'] == curr['categoria'] and last['submarca'] == curr['submarca'] and last['une'] == curr['une'] and last['mercado'] == curr['mercado']):
                        curr_table += 1
                        breakdown_tables.append([])
                    breakdown_tables[curr_table].append(breakdown_res[i])
                else:
                    curr_table = 0
                    breakdown_tables.append([])
                    breakdown_tables[curr_table].append(breakdown_res[i])

        responseObject = {
            'status': 'success',
            'table': table,
            'breakdown': breakdown_tables
        }
        return make_response(simplejson.dumps(responseObject)), 200


otb_view = OTB.as_view('otb')
otb_blueprint.add_url_rule(
    '/otb',
    view_func=otb_view,
    methods=['GET', 'POST']
)
