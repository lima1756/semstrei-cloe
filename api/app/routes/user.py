import logging
import jwt
from flask import Blueprint, request, make_response, jsonify, render_template
from flask_mail import Message
from fuzzywuzzy import fuzz

from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken
from app.models.RecoveryTokens import RecoveryTokens
from app.libs.decorators import admin_required
from app.libs.decorators import login_required
from app.libs import db, mail
from app.libs import validation

from .route_view import RouteView

user_blueprint = Blueprint('user', __name__)


class UserAPI(RouteView):

    def obtain_user_id_from_token(self):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]
        return UserData.decode_auth_token(auth_token)

    def get_user(self, id):
        user = UserData.query.get(id)
        if user:
            return self.return_success({
                'data': user.get_data_as_dict()
            })
        return self.return_not_found({
            'message': 'User not found'
        })

    def get_self_user(self):
        id = self.obtain_user_id_from_token()
        return self.get_user(id)

    @admin_required
    def search_user(self, search):
        users = UserData.query.all()
        output = []
        for user in users:
            print(user.email)
            print(fuzz.token_set_ratio(user.email, search))
            print(user.name)
            print(fuzz.token_set_ratio(user.name, search))
            print(user.phone_number)
            print(fuzz.token_set_ratio(user.phone_number, search))
            if fuzz.token_set_ratio(user.email, search) > 60 or fuzz.token_set_ratio(user.name, search) > 60 or fuzz.token_set_ratio(user.phone_number, search) > 60:
                output.append(user.get_data_as_dict())
        responseObject = {
            'status': 'success',
            'data': output
        }
        return make_response(jsonify(responseObject)), 200

    def switch_status(self, id, status=None):
        user = UserData.query.get(id)
        if user:
            user.enabled = (not user.enabled) if status is None else status
            db.session.add(user)
        else:
            raise IndexError("user with id "+str(id)+" not found")

    @admin_required
    def switch_multiple_status(self, status):
        try:
            data = request.get_json()
            users = data.get('users')
            count = 0
            if users is not None:
                for id in users:
                    try:
                        self.switch_status(id, status)
                        count += 1
                    except IndexError as e:
                        pass
            db.session.commit()
            return self.return_success_201({'updated': count})
        except:
            return self.return_server_error()

    @admin_required
    def switch_single_status(self, id, status=None):
        try:
            self.switch_status(id, status)
            db.session.commit()
            return self.return_success_201({'updated': 1})
        except IndexError:
            return self.return_not_found({
                'message': 'User doesn\'t exist'
            })
        except:
            return self.return_server_error()

    @admin_required
    def get_specific_user(self, id):
        return self.get_user(id)

    @admin_required
    def get_all_users(self):
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
        try:
            users = UserData.query.all()
            if page_size == -1:
                page_size = len(users)
            users_data = []
            for i in range(page * page_size, (page + 1) * page_size):
                if i >= len(users) or i < 0:
                    break
                user = users[i]
                users_data.append(user.get_data_as_dict())
            return self.return_success({
                'data': users_data
            })
        except Exception as e:
            logging.error(e)
            return self.return_server_error()

    def update_user(self, id):
        try:
            auth_token = request.headers.get('Authorization').split(" ")[1]
            resp = UserData.decode_auth_token(auth_token)
            curr_is_admin = UserData.query.get(resp).admin
            data = request.get_json()
            check = validation.InputValidation(data, {
                'email': [validation.Strip, validation.ValidateEmail],
                'password': [validation.Strip, validation.ValidatePassword],
                'name': [validation.Strip, validation.ValidateAlphabeticString],
                'phone_number': [validation.Strip, validation.ValidateInteger],
                'role': [validation.ValidateInteger],
            })
            try:
                data = check.validate()
            except validation.DataNotValidException:
                return self.return_data_not_valid(check)
            user = UserData.query.get(id)
            if user:
                if data.get('email'):
                    user.email = data.get('email')
                if data.get('password'):
                    user.set_password(data.get('password'))
                    user.new_user = False
                if data.get('name'):
                    user.name = data.get('name')
                if data.get('phone_number'):
                    user.phone_number = data.get('phone_number')
                if curr_is_admin and data.get('role') is not None:
                    user.role_id = data.get('role')
                    user.admin = data.get('role') == 0
                db.session.add(user)
                db.session.commit()
                return self.return_success(None)
            else:
                return self.return_not_found({
                    'message': 'no user found'
                })
        except Exception as e:
            logging.error(e)
            return self.return_server_error()

    @admin_required
    def update_user_admin(self, id):
        return self.update_user(id)

    @login_required
    @admin_required
    def post(self):
        data = request.get_json()
        user = UserData.query.filter_by(email=data.get('email')).first()
        role = data.get('role')
        if not user:
            check = validation.InputValidation(data, {
                'email': [validation.Strip, validation.ValidateNotEmpty, validation.ValidateEmail],
                'role': [validation.ValidateNotEmpty, validation.ValidateInteger],
                'name': [validation.Strip, validation.ValidateAlphabeticString],
                'phone_number': [validation.Strip, validation.ValidateInteger]
            })
            try:
                check.validate()
            except validation.DataNotValidException:
                return self.return_data_not_valid(check)
            plain_password = UserData.gen_password()
            email = data.get('email')
            name = data.get('name')
            try:
                user = UserData(
                    email=email,
                    password=plain_password,
                    name=name,
                    phone_number=data.get('phone_number'),
                    admin=(role == 0),
                    role=role
                )
                msg = Message(
                    'OTB: Welcome!',
                    sender='a01634417@itesm.mx',
                    recipients=[email]
                )
                msg.html = render_template(
                    "welcome.html",
                    name=name,
                    email=email,
                    password=plain_password
                )
                mail.send(msg)
                db.session.add(user)
                db.session.commit()
                return self.return_success({
                    'message': 'Successfully registered.'
                })
            except Exception as e:
                logging.error(e)
                return self.return_server_error()
        else:
            return self.return_response('fail', {'message': 'User already exists.'}, 409)

    @login_required
    def get(self, id, search):
        if id is None:
            return self.get_self_user()
        elif id == 'all':
            return self.get_all_users()
        elif id == 'search':
            return self.search_user(search)
        elif id.isnumeric():
            return self.get_specific_user(id)
        else:
            return self.return_response('fail', {'message': 'Not valid id.'}, 422)

    @login_required
    def put(self, action_or_id=None, id=None):
        if action_or_id == 'enable':
            if id is not None:
                return self.switch_single_status(id, True)
            else:
                return self.switch_multiple_status(True)
        elif action_or_id == 'disable':
            if id is not None:
                return self.switch_single_status(id, False)
            else:
                return self.switch_multiple_status(False)
        else:
            if action_or_id is None:
                return self.update_user(self.obtain_user_id_from_token())
            else:
                return self.update_user_admin(action_or_id)

    def delete_user(self, id):
        user = UserData.query.get(id)
        if user:
            db.session.delete(user)
        else:
            raise IndexError("user with id "+str(id)+" not found")

    @login_required
    @admin_required
    def delete(self, id):
        count = 0
        if id is None:
            data = request.get_json()
            users = data.get('users')
            if users is not None:
                for id in users:
                    try:
                        self.delete_user(id)
                        count += 1
                    except IndexError as e:
                        pass
        elif id.isnumeric():
            try:
                self.delete_user(id)
                count += 1
            except IndexError as e:
                return self.return_not_found({
                    'message': 'User doesn\'t exist'
                })
        else:
            return self.return_response('fail', {'message': 'Not valid id.'}, 422)
        db.session.commit()
        return self.return_success_201({
            'deleted': count
        })


# define the API resources
user_api = UserAPI.as_view('user_api')


# add Rules for API Endpoints
user_blueprint.add_url_rule(
    '/user',
    defaults={'id': None, 'search': None},
    view_func=user_api,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/user/<id>',
    defaults={'search': None},
    view_func=user_api,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/user/<id>/<search>',
    view_func=user_api,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/user/<id>',
    view_func=user_api,
    methods=['GET']
)
user_blueprint.add_url_rule(
    '/user',
    defaults={'id': None},
    view_func=user_api,
    methods=['DELETE']
)
user_blueprint.add_url_rule(
    '/user/<id>',
    view_func=user_api,
    methods=['DELETE']
)
user_blueprint.add_url_rule(
    '/user',
    view_func=user_api,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/user',
    defaults={'action_or_id': None, 'id': None},
    view_func=user_api,
    methods=['PUT']
)
user_blueprint.add_url_rule(
    '/user/<action_or_id>',
    defaults={'id': None},
    view_func=user_api,
    methods=['PUT']
)
user_blueprint.add_url_rule(
    '/user/<action_or_id>/<id>',
    view_func=user_api,
    methods=['PUT']
)
