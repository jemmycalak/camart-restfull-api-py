import jwt
from functools import wraps
from flask import request
from config import SECRET_KEY
from app.models.m_users import t_user

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'camart-token' in request.headers:
            token = request.headers['camart-token']

        if not token:
            resp = {'status':'false','msg':'Token is missing'}, 401
            return resp

        try:
            data = jwt.decode(token, SECRET_KEY)
            current_user = t_user.query.filter_by(id = data['userid']).first()
        except :
            resp = {'status':'false', 'msg':'Token is invalid'}, 401
            return resp

        return f(current_user, *args, **kwargs)
    return decorated