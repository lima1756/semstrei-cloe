from functools import wraps
from flask import make_response, request, jsonify

from app import App
from app.models.UserData import UserData
from app.models.BlacklistToken import BlacklistToken

app = App.get_instance().app

def admin_required(f):
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
            user = UserData.query.get(resp)
            if user.admin:
                return f(*args, **kwargs)
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User not admin'
                }
                return make_response(jsonify(responseObject)), 401
    return decorated_function
