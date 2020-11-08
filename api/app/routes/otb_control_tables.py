import logging
from flask import Blueprint, request, jsonify, make_response, render_template
from flask.views import MethodView
from app.models import ControlCategoryRateByUneAndPeriod, RelationClientMercado
from app.libs import db
from app.libs.decorators import login_required

otb_control_tables_blueprint = Blueprint('otb_control_tables', __name__)


class ControlTables(MethodView):

    def construct_object(self, data):
        pass

    def update_object(self, obj, data):
        pass

    def get_object(self, id):
        pass

    def get_all(self):
        pass

    def construct_json(self, obj):
        pass

    def get_all_users(self):
        page = request.args.get('page')
        page_size = request.args.get('page_size')
        if page is None and page_size is not None:
            page = 0
            page_size = int(page_size)
        elif page is not None and page_size is None:
            page_size = 10
            page = int(page)-1
        else:
            page = 0
            page_size = -1
        try:
            objs = self.get_all()
            if page_size == -1:
                page_size = len(objs)
            objs_data = []
            for i in range(page * page_size, (page + 1) * page_size):
                if i >= len(objs) or i < 0:
                    break
                obj = objs[i]
                objs_data.append(self.construct_json(obj))
            responseObject = {
                'status': 'success',
                'data': objs_data
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500

    @login_required
    def post(self, id):
        data = request.get_json()
        obj = self.construct_object(data)
        db.session.add(obj)
        db.session.commit()
        responseObject = {
            'status': 'success'
        }
        return make_response(jsonify(responseObject)), 201

    @login_required
    def put(self, id):
        data = request.get_json()
        obj = self.get_object(id)
        if obj is not None:
            obj = self.update_object(obj, data)
            db.session.add(obj)
            db.session.commit()
            responseObject = {
                'status': 'success'
            }
            return make_response(jsonify(responseObject)), 200
        else:
            responseObject = {
                'status': 'fail',
                'message': 'object not found'
            }
            return make_response(jsonify(responseObject)), 404

    @login_required
    def get(self, id):
        if id == 'all':
            return self.get_all_users()
        else:
            obj = self.get_object(id)
            if obj is not None:
                responseObject = {
                    'status': 'success',
                    'data': self.construct_json(obj)
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'object not found'
                }
                return make_response(jsonify(responseObject)), 404

    def delete_object(self, id):
        obj = self.get_object(id)
        if obj:
            db.session.delete(obj)
        else:
            raise IndexError("user with id "+str(id)+" not found")

    @login_required
    def delete(self, id):
        count = 0
        if id is None:
            data = request.get_json()
            objs = data.get('objects')
            if objs is not None:
                for id in objs:
                    try:
                        self.delete_object(id)
                        count += 1
                    except IndexError as e:
                        pass
        else:
            try:
                self.delete_object(id)
                count += 1
            except IndexError as e:
                responseObject = {
                    'status': 'fail',
                    'message': 'object not found'
                }
                return make_response(jsonify(responseObject)), 404
        db.session.commit()
        responseObject = {
            'status': 'success',
            'deleted': count
        }
        return make_response(jsonify(responseObject)), 200


class RelationClientMercadoRoute(ControlTables):

    def construct_object(self, data):
        return RelationClientMercado(
            data.get('client'),
            data.get('is_m1')
        )

    def update_object(self, obj, data):
        client = data.get('client')
        m1 = data.get('is_m1')
        if client:
            obj.client = client
        if m1:
            obj.isM1 = m1
        return obj

    def get_object(self, id):
        return RelationClientMercado.query.get(id)

    def construct_json(self, obj):
        return {
            'id': obj.id,
            'client': obj.client,
            'is_m1': obj.isM1
        }

    def get_all(self):
        return RelationClientMercado.query.all()


class RateByUneAndPeriod(ControlTables):

    def construct_object(self, data):
        return ControlCategoryRateByUneAndPeriod(
            data.get('month'),
            data.get('une'),
            float(data.get('rate')),
            data.get('date')
        )

    def update_object(self, obj, data):
        month = data.get('month')
        une = data.get('une')
        rate = data.get('rate')
        date = data.get('date')
        if month:
            obj.month = month
        if une:
            obj.une = une
        if rate:
            obj.rate_category_moda = float(rate)
        if date:
            obj.date = date
        return obj

    def get_object(self, id):
        return ControlCategoryRateByUneAndPeriod.query.get(id)

    def construct_json(self, obj):
        return {
            'id': obj.id,
            'month': obj.month,
            'une': obj.une,
            'rate': obj.rate_category_moda,
            'date': obj.date
        }

    def get_all(self):
        return ControlCategoryRateByUneAndPeriod.query.all()


relation_client_mercado_view = RelationClientMercadoRoute.as_view(
    'relation_client_mercado')
rate_by_une_view = RateByUneAndPeriod.as_view('rate_by_une')


otb_control_tables_blueprint.add_url_rule(
    '/otb/control/client_mercado',
    defaults={'id': None},
    view_func=relation_client_mercado_view,
    methods=['POST', 'DELETE']
)
otb_control_tables_blueprint.add_url_rule(
    '/otb/control/client_mercado/<id>',
    view_func=relation_client_mercado_view,
    methods=['GET', 'DELETE', 'PUT']
)

otb_control_tables_blueprint.add_url_rule(
    '/otb/control/rate_une',
    defaults={'id': None},
    view_func=rate_by_une_view,
    methods=['POST', 'DELETE']
)
otb_control_tables_blueprint.add_url_rule(
    '/otb/control/rate_une/<id>',
    view_func=rate_by_une_view,
    methods=['GET', 'DELETE', 'PUT']
)
