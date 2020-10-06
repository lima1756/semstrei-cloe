import logging
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.models import User, BlacklistToken
from app.decorators.admin_required import admin_required
from app.decorators.login_required import login_required
from app import db

user_management_blueprint = Blueprint('user_management', __name__)


class RegisterAPI(MethodView):
    @login_required
    @admin_required
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    admin=post_data.get('admin')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                # generate the auth token
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


class LoginAPI(MethodView):
    def post(self):
        # get the post data
        post_data = request.get_json()
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=post_data.get('email')
            ).first()
            if user.check_password(post_data.get('password')):
                if not user.enabled:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User disables.'
                    }
                    return make_response(jsonify(responseObject)), 401
                if post_data.get('keep'):
                    days_session = 30
                else:
                    days_session = 1
                auth_token = user.encode_auth_token(days_session)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode()
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500


class UserDataAPI(MethodView):
    @login_required
    def get(self):
        # get the auth token
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(id=resp).first()
            responseObject = {
                'status': 'success',
                'data': {
                    'user_id': user.id,
                    'email': user.email,
                    'admin': user.admin,
                    'enabled': user.enabled,
                    'registration_date': user.registered_on,
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401


class LogoutAPI(MethodView):
    """
    Logout Resource
    """

    def post(self):
        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    # insert the token
                    db.session.add(blacklist_token)
                    db.session.commit()
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged out.'
                    }
                    return make_response(jsonify(responseObject)), 200
                except Exception as e:
                    logging.error(e)
                    responseObject = {
                        'status': 'fail',
                        'message': e
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': resp
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return make_response(jsonify(responseObject)), 403


class RemoveUserAPI(MethodView):
    """
    Remove User
    """
    @login_required
    @admin_required
    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(
            id=post_data.get('id')
        ).first()
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


class SwitchUserStatus(MethodView):
    def switchUserStatus(self, status=None):
        post_data = request.get_json()
        user = User.query.filter_by(
            id=post_data.get('id')
        ).first()
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


class DisableAPI(SwitchUserStatus):
    """
    Disable User
    """
    @login_required
    @admin_required
    def post(self):
        return self.switchUserStatus(False)


class EnableAPI(SwitchUserStatus):
    """
    Enable User
    """
    @login_required
    @admin_required
    def post(self):
        return self.switchUserStatus(True)


class GetAllUsers(MethodView):
    @login_required
    @admin_required
    def get(self):
        post_data = request.get_json()
        if post_data:
            page = post_data.get('page') - 1
            page_size = post_data.get('page_size')
        else:
            page = 0
            page_size = 10
        users = User.query.all()
        users_data = []
        for i in range(page * page_size, (page + 1) * page_size):
            if i >= len(users) or i < 0:
                break
            user = users[i]
            users_data.append({
                'user_id': user.id,
                'email': user.email,
                'admin': user.admin,
                'enabled': user.enabled,
                'registration_date': user.registered_on,
            })
        responseObject = {
            'status': 'success',
            'data': users_data
        }
        return make_response(jsonify(responseObject)), 200



# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_data_view = UserDataAPI.as_view('user_data_api')
logout_view = LogoutAPI.as_view('logout_api')
remove_view = RemoveUserAPI.as_view('remove_api')
disable_view = DisableAPI.as_view('disable_api')
enable_view = EnableAPI.as_view('enable_api')
all_users = GetAllUsers.as_view('all_users')

# add Rules for API Endpoints
user_management_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/auth/remove',
    view_func=remove_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/auth/disable',
    view_func=disable_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/auth/enable',
    view_func=enable_view,
    methods=['POST']
)
user_management_blueprint.add_url_rule(
    '/user',
    view_func=user_data_view,
    methods=['GET']
)
user_management_blueprint.add_url_rule(
    '/users',
    view_func=all_users,
    methods=['GET']
)
