"""
This module defines the user auth decorator function

"""
from functools import wraps
from api.db_connection import conn
import jwt
from flask import request
from flask import jsonify
from api import secret_key
from api.endpoints.users import AuthUsers


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
            data = jwt.decode(token, secret_key, algorithm='HS256' )
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id=%s",(data['user_id'], ))
            current_user = cur.fetchall()
        except:
            return jsonify({'message':'Token is invalid!'}), 401
        return f(self, current_user, *args, **kwargs)
    return decorated
