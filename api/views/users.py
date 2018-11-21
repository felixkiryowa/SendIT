"""
This module defines api views
"""
from flask import request
from flask import jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from api import connection
from api.model.users import AuthUser
from api.validators.validate import user_auth_logic
from api.validators.validate import  check_for_empty_strings_in_reg_object
from api.validators.validate import check_if_posted_user_data_are_strings
from api.validators.validate import check_user_object_keys
from api.validators.validate import validating_email
from flask import json
from flask import Response

class AuthUsers(MethodView):
    """Class to define user auth end points"""
    def post(self):
        """funtion to register a new user"""
        rule = request.url_rule
        could_not_verify = "Invalid Username or Password"
        if 'signup' in rule.rule:
            new_user_data = request.get_json()
            return self.validate_posted_user_data(new_user_data)
        user_credentials = request.get_json()
        return AuthUser.execute_user_login_auth(
           self, user_credentials['username'], user_credentials['password'], could_not_verify
        )

    def validate_posted_user_data(self, new_user_data):
        """
        function to validate create new user object
        """
        if (validating_email(new_user_data['email'])):
            if (self.check_if_user_exists(new_user_data['username'], new_user_data['email'])):
                AuthUser(new_user_data['first_name'], new_user_data['last_name'], new_user_data['email'], 
                new_user_data['phone_contact'], new_user_data['username'], 
                generate_password_hash(new_user_data['user_password']), new_user_data['user_type']
                ).execute_add_new_user_query()
                return jsonify({'Message':'You registered successfully.'}),201   
            return jsonify({'Message':'User already exists'}),409
        return jsonify({'message':'Invalid email'}),400
       

    def check_if_user_exists(self, username, email):
        """
        method to check whether a user trying to register already exists in the database such that we dont
        re-register them again
        """
        # create a new cursor
        cur = connection.cursor()
        # execute the INSERT statement
        cur.execute("SELECT * FROM users WHERE username =%s AND email=%s",(username, email, ))
        fetch_user = cur.rowcount
        if fetch_user >= 1:
            return False
        return True
        