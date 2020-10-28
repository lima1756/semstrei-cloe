import logging
import jwt
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_mail import Message

from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken
from app.models.RecoveryTokens import RecoveryTokens
from app.decorators.admin_required import admin_required
from app.decorators.login_required import login_required
from app import App

user_blueprint = Blueprint('user', __name__)

mail = App.get_instance().mail
db = App.get_instance().db


class UserAPI(MethodView):

    def obtain_user_id_from_token(self):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]
        return UserData.decode_auth_token(auth_token)

    def get_user(self, id):
        user = UserData.query.get(id)
        if user:
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'phone_number': user.phone_number,
                    'admin': user.admin,
                    'enabled': user.enabled,
                    'registration_date': user.registered_on,
                    'role': user.role_id
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': 'There was a problem, please try again'
        }
        return make_response(jsonify(responseObject)), 401

    def get_self_user(self):
        id = self.obtain_user_id_from_token()
        return self.get_user(id)

    def switch_status(self, id, status=None):
        user = UserData.query.get(id)
        if user:
            user.enabled = (not user.enabled) if status is None else status
            db.session.add(user)
            db.session.commit()
            responseObject = {
                'status': 'success',
            }
            return make_response(jsonify(responseObject)), 201
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User doesn\'t exist'
            }
            return make_response(jsonify(responseObject)), 401

    @admin_required
    def get_specific_user(self, id):
        return self.get_user(id)

    @admin_required
    def get_all_users(self):
        page = request.args.get('page')
        page_size = request.args.get('page_size')
        if page is None:
            page = 0
        else:
            page = int(page)-1
        if page_size is None:
            page_size = 10
        else:
            page_size = int(page_size)
        users = UserData.query.all()
        users_data = []
        for i in range(page * page_size, (page + 1) * page_size):
            if i >= len(users) or i < 0:
                break
            user = users[i]
            users_data.append({
                'user_id': user.id,
                'email': user.email,
                'name': user.name,
                'phone_number': user.phone_number,
                'admin': user.admin,
                'enabled': user.enabled,
                'registration_date': user.registered_on,
                'role': user.role_id
            })
        responseObject = {
            'status': 'success',
            'data': users_data
        }
        return make_response(jsonify(responseObject)), 200

    def update_user(self, id):
        post_data = request.get_json()
        try:
            user = UserData.query.get(id)
            if user:
                if post_data.get('email'):
                    user.email = post_data.get('email')
                if post_data.get('password'):
                    user.set_password(post_data.get('password'))
                if post_data.get('name'):
                    user.name = post_data.get('name')
                if post_data.get('phone_number'):
                    user.phone_number = post_data.get('phone_number')
                db.session.add(user)
                db.session.commit()
                responseObject = {
                    'status': 'success'
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'success',
                    'message': 'no user found'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500

    @admin_required
    def update_user_admin(self, id):
        return self.update_user(id)

    @login_required
    @admin_required
    def post(self):
        post_data = request.get_json()
        user = UserData.query.filter_by(email=post_data.get('email')).first()
        role = post_data.get('role')
        if not user:
            try:
                user = UserData(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    name=post_data.get('name'),
                    phone_number=post_data.get('phone_number'),
                    admin=(role == 0),
                    role=role
                )
                db.session.add(user)
                db.session.commit()
                auth_token = user.encode_auth_token()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                logging.error(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return make_response(jsonify(responseObject)), 202

    @login_required
    def get(self, id):
        if id is None:
            return self.get_self_user()
        elif id == 'all':
            return self.get_all_users()
        else:
            return self.get_specific_user(id)

    @login_required
    def put(self, id, action):
        if action is None:
            if id is None:
                return self.update_user(self.obtain_user_id_from_token())
            else:
                return self.update_user_admin(id)
        else:
            if action == 'enable':
                return self.switch_status(id, True)
            elif action == 'disable':
                return self.switch_status(id, False)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'page not found'
                }
                return make_response(jsonify(responseObject)), 404

    @login_required
    @admin_required
    def delete(self, id):
        user = UserData.query.get(id)
        if user:
            db.session.delete(user)
            db.session.commit()
            responseObject = {
                'status': 'success',
            }
            return make_response(jsonify(responseObject)), 201
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User doesn\'t exist'
            }
            return make_response(jsonify(responseObject)), 401


# define the API resources
user_api = UserAPI.as_view('user_api')


# add Rules for API Endpoints
user_blueprint.add_url_rule(
    '/user',
    defaults={'id': None},
    view_func=user_api,
    methods=['GET', 'DELETE']
)
user_blueprint.add_url_rule(
    '/user/<id>',
    view_func=user_api,
    methods=['GET', 'POST', 'DELETE', 'PUT']
)
user_blueprint.add_url_rule(
    '/user',
    view_func=user_api,
    methods=['POST']
)
user_blueprint.add_url_rule(
    '/user',
    defaults={'id': None, 'action': None},
    view_func=user_api,
    methods=['PUT']
)
user_blueprint.add_url_rule(
    '/user/<id>',
    defaults={'action': None},
    view_func=user_api,
    methods=['PUT']
)
user_blueprint.add_url_rule(
    '/user/<id>/<action>',
    view_func=user_api,
    methods=['PUT']
)
