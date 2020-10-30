import logging
from functools import wraps
from flask import make_response, request, jsonify

from app import App
from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken

app = App.get_instance().app
db = App.get_instance().db

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            try:
                auth_token = auth_header.split(" ")[1]
            except IndexError:
                responseObject = {
                    'status': 'fail',
                    'message': 'Bearer token malformed.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            auth_token = ''
        if auth_token:
            resp = UserData.decode_auth_token(auth_token)
            if isinstance(resp, int):
                user = UserData.query.get(resp)
                if user and user.enabled:
                    return f(*args, **kwargs)
                else:
                    blacklist_token = BlacklistToken(token=auth_token)
                    try:
                        # insert the token
                        db.session.add(blacklist_token)
                        db.session.commit()
                    except Exception as e:
                        logging.error(e)
                    responseObject = {
                        'status': 'fail',
                        'message': 'There was a problem while logging in, please contact your administrator'
                    }
                    return make_response(jsonify(responseObject)), 403
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
            return make_response(jsonify(responseObject)), 401
    return decorated_function
