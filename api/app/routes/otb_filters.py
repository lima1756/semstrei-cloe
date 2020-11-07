from flask import Blueprint, request, jsonify, make_response, render_template
from flask.views import MethodView
from sqlalchemy.sql import func
from app.models.OtbResults import OtbResults
from app.libs import db

otb_filters_blueprint = Blueprint('otb', __name__)


class Filter(MethodView):
    def get_by_filter(self, filter):
        res_query = db.session.query(filter).group_by(filter).all()
        filter_data = []
        for row in res_query:
            filter_data.append(row[0])
        return filter_data

    def get(self):
        responseObject = {
            'status': 'success',
            'data': {
                'categoria': self.get_by_filter('categoria'),
                'une': self.get_by_filter('une'),
                'mercado': self.get_by_filter('mercado'),
                'submarca': self.get_by_filter('submarca'),
            }
        }
        return make_response(jsonify(responseObject)), 200


filter_view = Filter.as_view('filter')

otb_filters_blueprint.add_url_rule(
    '/otb/filters', view_func=filter_view, methods=['GET']
)
