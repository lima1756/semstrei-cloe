import logging
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken
from app.libs.decorators import login_required
from app.libs import db
from app.libs.validation import InputValidation, ValidateEmail, ValidatePassword, Strip

auth_blueprint = Blueprint('auth', __name__)


class Auth(MethodView):
    def login(self):
        data = request.get_json()
        try:
            user = UserData.query.filter_by(
                email=data.get('email')
            ).first()
            if user.check_password(data.get('password')):
                if not user.enabled:
                    responseObject = {
                        'status': 'fail',
                        'message': 'User disabled.'
                    }
                    return make_response(jsonify(responseObject)), 403
                if data.get('keep'):
                    days_session = 30
                else:
                    days_session = 1
                auth_token = user.encode_auth_token(days_session)
                if auth_token:
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode(),
                        'user': user.get_data_as_dict()
                    }
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 403
        except Exception as e:
            logging.error(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500

    @login_required
    def logout(self):
        auth_header = request.headers.get('Authorization')
        auth_token = auth_header.split(" ")[1]
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
                    'message': 'There was a problem, please try again'
                }
                return make_response(jsonify(responseObject)), 500
        else:
            responseObject = {
                'status': 'fail',
                'message': 'Token not valid'
            }
            return make_response(jsonify(responseObject)), 400

    def post(self, action):
        if action == 'login':
            return self.login()
        elif action == 'logout':
            return self.logout()
        else:
            responseObject = {
                'status': 'fail',
                'message': 'page not found'
            }
            return make_response(jsonify(responseObject)), 404


auth_api = Auth.as_view('auth_api')

auth_blueprint.add_url_rule(
    '/auth/<action>',
    view_func=auth_api,
    methods=['POST']
)
