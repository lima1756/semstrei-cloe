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

user_management_blueprint = Blueprint('user_management', __name__)

mail = App.get_instance().mail
db = App.get_instance().db

class RegisterAPI(MethodView):
    @login_required
    @admin_required
    def post(self):
        # get the post data
        post_data = request.get_json()
        # check if user already exists
        user = UserData.query.filter_by(email=post_data.get('email')).first()
        role=post_data.get('role')
        if not user:
            try:
                user = UserData(
                    email=post_data.get('email'),
                    password=post_data.get('password'),
                    name=post_data.get('name'),
                    phone_number=post_data.get('phone_number'),
                    admin=(role==0),
                    role=role
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
            user = UserData.query.filter_by(
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
        resp = UserData.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = UserData.query.filter_by(id=resp).first()
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
            resp = UserData.decode_auth_token(auth_token)
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
        user = UserData.query.filter_by(
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
        user = UserData.query.filter_by(
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


class RequestRecoverPassword(MethodView):
    
    def get(self):
        try:
            email = request.args.get('email')
            user = UserData.query.filter_by(
                email=email
            ).first()
            if user:
                token = RecoveryTokens(user)
                db.session.add(token)
                db.session.commit()
                msg = Message(
                    'OTB: Recover your password', 
                    sender = 'a01634417@itesm.mx', 
                    recipients = [email]
                )
                msg.body = token.key
                mail.send(msg)
                responseObject = {
                    'status': 'success'
                }
                return make_response(jsonify(responseObject)), 200
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'There was a problem, please try again'
            }
            return make_response(jsonify(responseObject)), 500
        responseObject = {
            'status': 'fail',
            'message': 'There was a problem, please try again.'
        }
        return make_response(jsonify(responseObject)), 500


class RecoverPassword(MethodView):

    def get(self):
        try:
            token = RecoveryTokens.query.filter_by(
                key=request.args.get('token')
            ).first()
            if token:
                RecoveryTokens.validate_key(token.key)
                responseObject = {
                    'status': 'success'
                }
                return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Token not found'
                }
                return make_response(jsonify(responseObject)), 404
        except jwt.ExpiredSignatureError:
            responseObject = {
                'status': 'fail',
                'message': 'Token expired. Please click on forgot password again.'
            }
            return make_response(jsonify(responseObject)), 401
        except jwt.InvalidTokenError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid token. Please click on forgot password again'
            }
            return make_response(jsonify(responseObject)), 401
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'There was a problem, please try again'
            }
            return make_response(jsonify(responseObject)), 500

    def put(self):
        try:
            post_data = request.get_json()
            token = RecoveryTokens.query.filter_by(
                key=request.args.get('token')
            ).first()
            if token is None:
                responseObject = {
                    'status': 'fail',
                    'message': 'Invalid token. Please request a new email'
                }
                return make_response(jsonify(responseObject)), 401
            if token.used:
                responseObject = {
                    'status': 'fail',
                    'message': 'Link already used, please request a new one.'
                }
                return make_response(jsonify(responseObject)), 401
            user_id = RecoveryTokens.validate_key(token.key)
            user = UserData.query.filter_by(
                id=user_id
            ).first()
            if user is None:
                responseObject = {
                    'status': 'fail',
                    'message': 'There was a problem, resetting your user, please contact your administrator.'
                }
                return make_response(jsonify(responseObject)), 401

            user.set_password(post_data.get('password'))
            token.used = True
            db.session.add(user)
            db.session.add(token)
            db.session.commit()
            responseObject = {
                'status': 'success'
            }
            return make_response(jsonify(responseObject)), 200               
        except jwt.ExpiredSignatureError:
            responseObject = {
                'status': 'fail',
                'message': 'Token expired. Please click on forgot password again.'
            }
            return make_response(jsonify(responseObject)), 401
        except jwt.InvalidTokenError:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid token. Please request a new email'
            }
            return make_response(jsonify(responseObject)), 401
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500    


# define the API resources
registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_data_view = UserDataAPI.as_view('user_data_api')
logout_view = LogoutAPI.as_view('logout_api')
remove_view = RemoveUserAPI.as_view('remove_api')
disable_view = DisableAPI.as_view('disable_api')
enable_view = EnableAPI.as_view('enable_api')
all_users = GetAllUsers.as_view('all_users')
request_recover_password = RequestRecoverPassword.as_view('request_recover_password')
recover_password = RecoverPassword.as_view('recover_password')

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
user_management_blueprint.add_url_rule(
    '/auth/request_recover',
    view_func=request_recover_password,
    methods=['GET']
)
user_management_blueprint.add_url_rule(
    '/auth/recover',
    view_func=recover_password,
    methods=['GET', 'PUT']
)
