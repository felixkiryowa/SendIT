"""
This module defines api views
"""
from flask import request
from flask.views import MethodView
from api.model.users import AuthUser
from api.validators.validate import validate_posted_user_data, user_auth_logic


class AuthUsers(MethodView):
    """Class to define user auth end points"""
    users = []
    def post(self):
        """funtion to register a new user"""
        rule = request.url_rule
        could_not_verify = "Wrong Username and Password"
        if 'signup' in rule.rule:
            user_signup_object = request.get_json() 
            return validate_posted_user_data(self.users, user_signup_object)
        return user_auth_logic(self.users, could_not_verify)
        