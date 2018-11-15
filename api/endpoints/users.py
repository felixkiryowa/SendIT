"""
This module defines api views

"""
import datetime
from flask import jsonify, request, Response , json
from flask.views import MethodView
from api.model.users import AuthUser
from api.validators.validate import validate_posted_user_data, user_auth_logic


class AuthUsers(MethodView):
    """Class to define user auth end points"""
    user = AuthUser(
        1, "stella", "ssendawula", "stella@gmail.com", "0700978654", "stella22", "email@123", "admin"
    )
    
    users = [user]
   
    def post(self):
        """funtion to register a new user"""
        rule = request.url_rule
        could_not_verify = "Wrong Username and Password"
        if 'signup' in rule.rule:     
            return validate_posted_user_data(self.users)
        return user_auth_logic(self.users, could_not_verify)
        