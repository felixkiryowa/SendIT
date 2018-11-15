"""
This module defines the user auth decorator function

"""
from functools import wraps
import jwt
from flask import request
from flask import jsonify
from api import secret_key
from api.endpoints.users import AuthUsers

AUTH_USERS = AuthUsers()

def token_required(f):
    """
    function to handler user authentications to API endpoints
    """
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = None
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message':'Token is missing!'}), 401
        try:
            data = jwt.decode(token, secret_key, algorithm='HS256')
            user_username = data['username']
            users_list = AUTH_USERS .users
            for user in users_list:
                if user_username == user.__dict__['username']:
                    current_user = user
        except:
            return jsonify({'message':'Token is invalid!'}), 401
        return f(self, current_user, *args, **kwargs)
    return decorated
