import logging
from flask import request as req
from app import app
from app.models import User

def log(user_id):
    ip = req.environ['REMOTE_ADDR'] if req.environ.get(
        'HTTP_X_FORWARDED_FOR') is None else req.environ['HTTP_X_FORWARDED_FOR']
    url = req.base_url
    logging.info(
        ip + ' - - User: ' + user_id + ' - Request: ' + url + '')

@app.before_request
def event_logger():
    auth = req.headers.get('Authorization')
    if auth:
        token = auth.split(" ")[1]
        user_id = User.decode_auth_token(token)
        if isinstance(user_id, int):
            log(str(user_id))
        else:
            log('None')
    else:
        log('None')
