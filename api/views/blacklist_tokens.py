"""
This module defines api views

"""
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.model.black_list_tokens import BlackListTokens



class BlacklistToken(MethodView):
    """Class to define all the api end points"""
    def post(self):
        """funtion to place a new order"""
        used_token = (request.get_json())["user_token"]
        return BlackListTokens(
            used_token
        ).execute_save_used_token_query() 
