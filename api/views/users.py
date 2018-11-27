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
from api.validators.validate import Validators

class AuthUsers(MethodView):
    """Class to define user auth end points"""
    @swag_from('../docs/signup_login.yml')
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
        try:
            first_name = new_user_data['first_name'].strip()
            last_name =  new_user_data['last_name'].strip()
            email = new_user_data['email'].strip()
            phone_contact = new_user_data['phone_contact'].strip()
            username = new_user_data['username'].strip()
            user_password = new_user_data['user_password'].strip()
        except:
            return jsonify({'message':'One or More Fields Are Missing'}),400
        if (not first_name  or not last_name or not email or not phone_contact or not 
        username or not user_password):
            return jsonify({'message':'One or More Fields Are Empty field'}), 400
        if not (Validators().search_username_are_only_characters(new_user_data['first_name'], 
        new_user_data['last_name'])):
            return jsonify({'message':'One Or More Fields consist of regular expressions'}), 400
        if not (Validators().validate_phone_number_consist_of_digits(new_user_data['phone_contact'])):
            return jsonify({'message': 'Phone contact should consist of only digits'}), 400
        if not (Validators().validate_length_of_phone_number(new_user_data['phone_contact'])):
            return jsonify({'message': 'Phone contact should consist of 10 digits'}), 400
        if not (Validators().validate_email(new_user_data)):
            return jsonify({'message':'Invalid email'}), 400
        if (Validators().check_if_user_exists(new_user_data['username'], new_user_data['email'])):
            return self.execute_add_new_user_logic(new_user_data)
        return jsonify({'Message':'User already exists'}),409

    def execute_add_new_user_logic(self, new_user_data):
        """
        method to register new user 
        """
        user_role = 'user'
        AuthUser(new_user_data['first_name'], new_user_data['last_name'], new_user_data['email'], 
        new_user_data['phone_contact'], new_user_data['username'], 
        generate_password_hash(new_user_data['user_password']), user_role
        ).execute_add_new_user_query()
        return jsonify({'Message':'You registered successfully.'}),201 
        

   

    
        