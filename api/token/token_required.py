import jwt
import os
import logging
from flask import request
from flask import jsonify
from functools import wraps 
from api.endpoints.users import AuthUsers

auth_users = AuthUsers()

def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = None
        secret_key = os.getenv('APP_SECRET_KEY')
        if 'token' in request.headers:
            token = request.headers['token']
        if not token:
            return jsonify({'message':'Token is missing!'}),401
        try:
            data = jwt.decode(token, secret_key,  algorithm='HS256')
            user_username = data['username']
            logging.info(user_username)
            users_list = auth_users.users
            for user in users_list:
                if user_username == user.__dict__['username']:
                    current_user = user
        except:
            return jsonify({'message':'Token is invalid!'}),401
        return f(self, current_user, *args, **kwargs)
    return decorated