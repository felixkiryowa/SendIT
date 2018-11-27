"""
This module defines the user auth decorator function

"""
from functools import wraps
from api import connection
import jwt
from flask import request
from flask import jsonify
from api import secret_key
from api.views.users import AuthUsers


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
            return jsonify({'message':'Token is required to perform this action!'}), 401
        try:
            data = jwt.decode(token, secret_key, algorithm='HS256' )
            cur = connection.cursor()
            cur.execute("SELECT * FROM users WHERE user_id=%s",(data['user_id'], ))
            current_user = cur.fetchall()
        except:
            return jsonify({'message':'Token has expired,please login again'}), 401
        return f(self, current_user, *args, **kwargs)
    return decorated
