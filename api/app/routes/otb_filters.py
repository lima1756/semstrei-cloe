from flask import Blueprint, request, jsonify, make_response, render_template
from .route_view import RouteView
from sqlalchemy.sql import func
from app.models.OtbResults import OtbResults
from app.libs import db
from app.libs.decorators import login_required
import datetime

otb_filters_blueprint = Blueprint('otb_filters', __name__)


class Filter(RouteView):

    filters = {
        'categoria': OtbResults.categoria,
        'une': OtbResults.une,
        'mercado': OtbResults.mercado,
        'submarca': OtbResults.submarca,
        'startDateCurrentPeriodOTB': OtbResults.startDateCurrentPeriodOTB
    }

    def format_date(self, date_raw):
        date = datetime.datetime.strptime(
            date_raw.isoformat(), '%Y-%m-%dT%H:%M:%S')
        return date.strftime('%d-%b-%y')

    def get_by_filter(self, filter, formatter = None):
        res_query = db.session.query(
            self.filters[filter]).group_by(filter).all()
        filter_data = []
        for row in res_query:
            if formatter is not None:
                data = formatter(row[0])
            else:
                data = row[0]
            filter_data.append(data)
        return filter_data

    @login_required
    def get(self):
        responseObject = {
            'status': 'success',
            'filters': {
                'categoria': self.get_by_filter('categoria'),
                'une': self.get_by_filter('une'),
                'mercado': self.get_by_filter('mercado'),
                'submarca': self.get_by_filter('submarca'),
                'periodo': self.get_by_filter('startDateCurrentPeriodOTB', self.format_date),
            }
        }
        return make_response(jsonify(responseObject)), 200


filter_view = Filter.as_view('filter')

otb_filters_blueprint.add_url_rule(
    '/otb/filters', view_func=filter_view, methods=['GET']
)
