"""
This module defines api views
"""
import re
from flasgger import swag_from
from flask import request
from flask import jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from api import connection
from api.model.users import AuthUser
from validate_email import validate_email
from flask import json
from flask import Response

class AuthUsers(MethodView):
    """Class to define user auth end points"""
    @swag_from('../docs/signup_login.yml')
    def post(self):
        """funtion to register a new user"""
        rule = request.url_rule
        could_not_verify = "Invalid Username or Password"
        if 'signup' in rule.rule:
            new_user_data = request.get_json()
            if (self.check_if_user_exists(new_user_data['username'], new_user_data['email'])):
                return self.validate_posted_user_data(new_user_data)
            return jsonify({'Message':'User already exists'}),409
        user_credentials = request.get_json()
        return AuthUser.execute_user_login_auth(
           self, user_credentials['username'], user_credentials['password'], could_not_verify
        )

    def validate_posted_user_data(self, new_user_data):
        """
        function to validate create new user object
        """
        if(self.check_posted_order_object_for_keys(new_user_data) and  
        self.search_regular_expression_characters(new_user_data) and self.validate_phone_number_consist_of_digits(new_user_data)):
            if (self.validating_email(new_user_data['email'])):
                if (self.check_if_user_exists(new_user_data['username'], new_user_data['email'])):
                    return self.execute_add_new_user_logic(new_user_data)   
            return jsonify({'message':'Invalid email'}),400
        register_user_object = "{'first_name': 'fred','last_name': 'kijjambu','email': 'fredk@gmail.com','phone_contact': '0789346789',\
        'username': 'fkijjambu22','user_password': 'user123'}"
        bad_order_object = {
        "Invalid_user_object":register_user_object
        }
        response = Response(
            json.dumps(bad_order_object),
            status=400, mimetype="application/json"
            )
        return response
        

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

    def execute_add_new_user_logic(self, new_user_data):
        AuthUser(new_user_data['first_name'], new_user_data['last_name'], new_user_data['email'], 
        new_user_data['phone_contact'], new_user_data['username'], 
        generate_password_hash(new_user_data['user_password']), new_user_data['user_type']
        ).execute_add_new_user_query()
        return jsonify({'Message':'You registered successfully.'}),201   
        

    def validating_email(self, user_email):
        """
        function to validate email of the user
        """
        return (validate_email(user_email))

    def check_posted_order_object_for_keys(self, new_user_data):
        """
        method to check for keys in a posted user object
        """
        order_keys = [
            'first_name', 'last_name',
            'email',
            'phone_contact',
            'username', 'user_password', 'user_type'
        ]
        if set(order_keys).issubset(new_user_data):
            return True
        return False

    def search_regular_expression_characters(self, new_user_data):
        """
        method to search for regular expressions in posted user data
        """
        #create a regular expression object to be used in matching
        regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]') 
        #check if a posted order data contails regular expressions
        if (regex.search(new_user_data['first_name']) is None and regex.search(new_user_data['last_name']) is None 
        and regex.search(new_user_data['phone_contact']) is None
        and regex.search(new_user_data['username']) is None and regex.search(new_user_data['user_password']) is None and
        regex.search(new_user_data['user_type']) is None):       
            return True  
        return False 

    def validate_phone_number_consist_of_digits(self, new_user_data):
        """
        method to check whether a phone contact consist of only digits
        """
        if(new_user_data['phone_contact'].isdigit() and len(new_user_data['phone_contact']) == 10):
            return True
        return False

    
        