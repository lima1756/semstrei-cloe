import logging
from flask import Blueprint, request, jsonify, make_response, render_template
from .route_view import RouteView
from app.models import ControlCategoryRateByUneAndPeriod, RelationClientMercado
from app.libs import db
from app.libs.decorators import login_required
from app.libs import validation

otb_control_tables_blueprint = Blueprint('otb_control_tables', __name__)


class ControlTables(RouteView):

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

    def get_all_objects(self):
        page = request.args.get('page')
        page_size = request.args.get('page_size')
        if page is None and page_size is not None:
            page = 0
            page_size = int(page_size)
        elif page is not None and page_size is None:
            page_size = 10
            page = int(page)-1
        elif page is None and page_size is None:
            page = 0
            page_size = -1
        else:
            page = int(page)-1
            page_size = int(page_size)
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
            return self.return_success({
                'data': objs_data
            })
        except Exception as e:
            logging.error(e)
            return self.return_server_error()

    @login_required
    def post(self, id):
        data = request.get_json()
        obj = self.construct_object(data)
        db.session.add(obj)
        db.session.commit()
        return self.return_success_201()

    @login_required
    def put(self, id):
        data = request.get_json()
        if id.isnumeric():
            obj = self.get_object(id)
            if obj is not None:
                obj = self.update_object(obj, data)
                db.session.add(obj)
                db.session.commit()
                return self.return_success()
        return self.return_not_found({
            'message': 'object not found'
        })

    @login_required
    def get(self, id):
        if id == 'all':
            return self.get_all_objects()
        elif id.isnumeric():
            obj = self.get_object(id)
            if obj is not None:
                return self.return_success({'data': self.construct_json(obj)
                                            })
        return self.return_not_found({'message': 'object not found'})

    def delete_object(self, id):
        if id.isnumeric():
            obj = self.get_object(id)
            if obj:
                db.session.delete(obj)
                return
        raise IndexError("object with id "+str(id)+" not found")

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
        elif id.isnumeric():
            try:
                self.delete_object(id)
                count += 1
            except IndexError as e:
                return self.return_not_found({'message': 'object not found'})
        else:
            return self.return_not_found({'message': 'object not found'})
        db.session.commit()
        return self.return_success({'deleted': count})


class RelationClientMercadoRoute(ControlTables):

    def construct_object(self, data):
        check = validation.InputValidation(data, {
            'client': [validation.Strip, validation.ValidateNotEmpty],
            'is_m1': [validation.ValidateNotEmpty]
        })
        try:
            data = check.validate()
        except validation.DataNotValidException:
            return self.return_data_not_valid(check)
        return RelationClientMercado(
            data.get('client'),
            data.get('is_m1')
        )

    def update_object(self, obj, data):
        check = validation.InputValidation(data, {
            'client': [validation.Strip, validation.ValidateNotEmpty],
            'is_m1': [validation.ValidateNotEmpty]
        })
        try:
            data = check.validate()
        except validation.DataNotValidException:
            return self.return_data_not_valid(check)
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

    def validate_input(self, data):
        check = validation.InputValidation(data, {
            'month': [validation.Strip, validation.ValidateNotEmpty],
            'une': [validation.Strip, validation.ValidateNotEmpty],
            'rate': [validation.ValidateNumber],
            'date': [validation.Strip]
        })
        return check

    def construct_object(self, data):
        try:
            check = self.validate_input(data)
            data = check.validate()
        except validation.DataNotValidException:
            return self.return_data_not_valid(check)
        return ControlCategoryRateByUneAndPeriod(
            data.get('month'),
            data.get('une'),
            float(data.get('rate')),
            data.get('date')
        )

    def update_object(self, obj, data):
        try:
            check = self.validate_input(data)
            data = check.validate()
        except validation.DataNotValidException:
            return self.return_data_not_valid(check)
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
