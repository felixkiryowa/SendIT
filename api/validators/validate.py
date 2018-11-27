"""
This module defines a class for validators
"""
import re
from flask import  request
from api import connection
class Validators:
    """
    class to define classes of validators
    """
    def check_if_user_exists(self, username, email):
        """
        method to check whether a user trying to register already exists in the database such that we dont
        re-register them again
        """
        # create a new cursor
        cursor = connection.cursor()
        # execute the INSERT statement
        cursor.execute("SELECT * FROM users WHERE username =%s AND email=%s",(username, email, ))
        fetch_user = cursor.rowcount
        if fetch_user >= 1:
            return False
        return True

    def execute_add_new_user_logic(self, new_user_data):
        user_role = 'user'
        AuthUser(new_user_data['first_name'], new_user_data['last_name'], new_user_data['email'], 
        new_user_data['phone_contact'], new_user_data['username'], 
        generate_password_hash(new_user_data['user_password']), user_role
        ).execute_add_new_user_query()
        return jsonify({'Message':'You registered successfully.'}),201   
        

    def validate_email(self, new_user_data):
        """
        function to validate email of the user
        """
        pattern = re.compile(r"^[A-Za-z0-9.+_-]+@[A-Za-z0-9._-]+\.[a-zA-Z]*$")
        if not pattern.match(new_user_data['email']):
            return False
        return True


    def check_posted_order_object_for_keys(self, new_user_data):
        """
        method to check for keys in a posted user object
        """
        order_keys = [
            'first_name', 
            'last_name',
            'email',
            'phone_contact',
            'username', 
            'user_password'
        ]
        
        if set(order_keys).issubset(new_user_data):
            return True
        return False

    def search_username_are_only_characters(self, firstname, lastname):
        """
        method to search for regular expressions in posted user data
        """
        #create a regular expression object to be used in matching
        first_name_regex = re.compile(r"^[A-Za-z\s]{4,30}$")
        last_name_regex = re.compile(r"^[A-Za-z\s]{4,30}$") 

        #check if a posted order data contails regular expressions
        if (first_name_regex.match(firstname) and last_name_regex.match(lastname)):      
            return True
        return False

    def validate_phone_number_consist_of_digits(self, phone_contact):
        """
        method to check whether a phone contact consist of only digits
        """
        if(phone_contact.isdigit()):
            return True
        return False
    def validate_length_of_phone_number(self, phone_contact):
        """
        method to validate the length of a phone contact
        """
        if(len(phone_contact) == 10):
            return True
        return False
