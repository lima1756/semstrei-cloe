import logging
import jwt
from flask import Blueprint, request, make_response, jsonify, render_template
from flask.views import MethodView
from flask_mail import Message

from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken
from app.models.RecoveryTokens import RecoveryTokens
from app.libs.decorators import admin_required
from app.libs.decorators import login_required
from app.libs import db, mail

user_blueprint = Blueprint('user', __name__)


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
                'data': user.get_data_as_dict()
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': 'User not found'
        }
        return make_response(jsonify(responseObject)), 404

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
            return make_response(jsonify(responseObject)), 404

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
        else:
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
            responseObject = {
                'status': 'success',
                'data': users_data
            }
            return make_response(jsonify(responseObject)), 200
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 500

    def update_user(self, id):
        try:
            auth_token = request.headers.get('Authorization').split(" ")[1]
            resp = UserData.decode_auth_token(auth_token)
            curr_is_admin = UserData.query.get(resp).admin
            data = request.get_json()
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
            plain_password = UserData.gen_password()
            email = post_data.get('email')
            name = post_data.get('name')
            try:
                user = UserData(
                    email=email,
                    password=plain_password,
                    name=name,
                    phone_number=post_data.get('phone_number'),
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
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                logging.error(e)
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return make_response(jsonify(responseObject)), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists.',
            }
            return make_response(jsonify(responseObject)), 409

    @login_required
    def get(self, id):
        if id is None:
            return self.get_self_user()
        elif id == 'all':
            return self.get_all_users()
        else:
            return self.get_specific_user(id)

    @login_required
    def put(self, id=None, action=None):
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
            return make_response(jsonify(responseObject)), 404


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
