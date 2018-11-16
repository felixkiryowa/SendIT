
from flask import request

def check_if_posted_user_data_are_not_empty_strings():
    """
    function to check whether posted object has got no empty strings
    """
    return (request.json['first_name'] != '' and request.json['last_name'] != ''
    and request.json['email'] != '' and request.json['contact'] != ''
    and request.json['username'] != '' and  
    request.json['password'] != '' and request.json['user_type'] != '' )