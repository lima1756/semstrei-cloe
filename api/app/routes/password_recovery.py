import logging
import jwt
from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView
from flask_mail import Message

from app.models.UserData import UserData
from app.models.RecoveryTokens import RecoveryTokens
from app import App

password_recovery_blueprint = Blueprint('passsword_recovery', __name__)

mail = App.get_instance().mail
db = App.get_instance().db


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
                    sender='a01634417@itesm.mx',
                    recipients=[email]
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
            user = UserData.query.get(user_id)
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


request_recover_password = RequestRecoverPassword.as_view(
    'request_recover_password')
recover_password = RecoverPassword.as_view('recover_password')

password_recovery_blueprint.add_url_rule(
    '/recover/request',
    view_func=request_recover_password,
    methods=['GET']
)
password_recovery_blueprint.add_url_rule(
    '/recover',
    view_func=recover_password,
    methods=['GET', 'PUT']
)
