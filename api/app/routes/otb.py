from flask import Blueprint, request, make_response, render_template
from flask.views import MethodView
from sqlalchemy import asc
from sqlalchemy.sql import func
from app.models.OtbResults import OtbResults
from app.libs import db
from app.libs.decorators import login_required
from flask_weasyprint import HTML, render_pdf
import simplejson
import datetime

otb_blueprint = Blueprint('otb', __name__)


class OTB(MethodView):

    def format_date(self, date_raw):
        date = datetime.datetime.strptime(
            date_raw.isoformat(), '%Y-%m-%dT%H:%M:%S')
        month = date.strftime("%b")
        if month == "Jan":
            month = "Ene"
        elif month == "Apr":
            month = "Abr"
        elif month == "Aug":
            month = "Ago"
        elif month == "Dec":
            month = "Dic"
        return date.strftime('%d-') + month + date.strftime("-%Y")

    def format_period_length(self, raw):
        period_length = str(raw) + " dias"
        if raw == 1:
            period_length = "1 dia"
        elif raw == 7:
            period_length = "1 semana"
        elif raw == 14:
            period_length = "2 semanas"
        elif raw == 30 or raw == 28 or raw == 29 or raw == 31:
            period_length = "1 mes"
        return period_length

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
            OtbResults.daysLongCurrentPeriodOTB,
        ]

        # WHERE
        filters = [
            # OtbResults.isFutureProjection == False,
            OtbResults.startDateProjectionPeriodOTB == current_period
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
            OtbResults.startDateCurrentPeriodOTB,
            OtbResults.startDateProjectionPeriodOTB,
            OtbResults.daysLongCurrentPeriodOTB
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

        order_by.append(asc(OtbResults.startDateCurrentPeriodOTB))

        res_query = db.session.query(*select)\
            .filter(*filters).group_by(*group_by)\
            .order_by(*order_by).all()
        response = []
        for row in res_query:
            period_length = self.format_period_length(row[11])
            response.append({
                "startDateCurrentPeriodOTB": self.format_date(row[1]),
                "startDateProjectionPeriodOTB": self.format_date(row[0]),
                "initialStock": row[2],
                "inventoryOnStores": row[3],
                "purchases": row[4],
                "devolution": row[5],
                "targetSells": row[6],
                "targetStock": row[7],
                "projectionEomStock": row[8],
                "otb_minus_ctb": row[9],
                "percentage_otb": row[10],
                "period_length": period_length,
                "categoria": row[12] if len(row) > 12 else categoria,
                "submarca": row[13] if len(row) > 13 else submarca,
                "une": row[14] if len(row) > 14 else une,
                "mercado": row[15] if len(row) > 15 else mercado,
            })
        return response

    def get_response_obj(self, categoria, une, submarca, mercado, current_period, breakdown):
        table = self.get_table(categoria, submarca, une,
                               mercado, current_period)
        breakdown_tables = None
        if breakdown:
            breakdown_tables = []
            curr_table = -1
            breakdown_res = self.get_table(categoria, submarca, une,
                                           mercado, current_period, True)
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
        return responseObject

    def gen_pdf(self, tables, filters):
        html = render_template("otb_pdf.html", table=tables['table'], filters="todo", breakdown=tables['breakdown'])
        return render_pdf(HTML(string=html), download_filename="reporte.pdf")

    @login_required
    def get(self):
        categoria = request.args.get('categoria')
        une = request.args.get('une')
        submarca = request.args.get('submarca')
        mercado = request.args.get('mercado')
        current_period = request.args.get('current_period')
        breakdown = request.args.get('breakdown') == 'True'
        pdf = request.args.get('pdf') == 'True'
        responseObject = self.get_response_obj(categoria, une, submarca, mercado, current_period, breakdown)
        if pdf:
            filters = ""
            if une is not None:
                filters += une + " | "
            if submarca is not None:
                filters += submarca + " | "
            if categoria is not None:
                filters += categoria + " | "
            if mercado is not None:
                filters += mercado + " | "
            if filters == "":
                filters = "Todo el inventario"
            else: 
                filters = filters[:-3]
            return self.gen_pdf(responseObject, filters)
        else:
            return make_response(simplejson.dumps(responseObject)), 200


otb_view = OTB.as_view('otb')
otb_blueprint.add_url_rule(
    '/otb',
    view_func=otb_view,
    methods=['GET', 'POST']
)
