"""
This module defines api views
"""
from flask import request
from flask import jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from api.db_connection import conn
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
    users = []
    def post(self):
        """funtion to register a new user"""
        rule = request.url_rule
        could_not_verify = "Invalid Username and Password"
        if 'signup' in rule.rule:
            AuthUser.create_users_table()
            new_user_data = request.get_json()
            user_type = 'user'
            return self.validate_posted_user_data(new_user_data, user_type)
        user_credentials = request.get_json()
        return AuthUser.execute_user_login_auth(
           self, user_credentials['username'], user_credentials['password'], could_not_verify
        )

    def validate_posted_user_data(self, new_user_data, user_type):
        """
        function to validate create new user object
        """
        if (check_for_empty_strings_in_reg_object('first_name', 'last_name', 'email', 
        'phone_contact', 'username', 'user_password') and
        check_user_object_keys(new_user_data)):
            if (validating_email(new_user_data['email'])):
                if (self.check_if_user_exists(new_user_data['username'], new_user_data['email'])):
                    AuthUser(new_user_data['first_name'], new_user_data['last_name'], new_user_data['email'], 
                    new_user_data['phone_contact'], new_user_data['username'], 
                    generate_password_hash(new_user_data['user_password']), user_type
                    ).execute_add_new_user_query()
                    return jsonify({'Message':'You registered successfully.'}),201   
                return jsonify({'Message':'User already exists'}),409
            return jsonify({'message':'Invalid email'}),400
        user_posted_object = "{'first_name': 'julius','last_name': 'kasagala','email': 'jk@gmail.com',\
        'contact': '070786543','username': 'kas1234','password': 'kas@123'}"
        bad_order_object = {
        "Valid_user_object":user_posted_object
        }
        response = Response(
            json.dumps(bad_order_object),
            status=400, mimetype="application/json"
            )
        return response

    def check_if_user_exists(self, username, email):
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("SELECT * FROM users WHERE username =%s AND email=%s",(username, email, ))
        fetch_user = cur.rowcount
        if fetch_user >= 1:
            return False
        return True
        