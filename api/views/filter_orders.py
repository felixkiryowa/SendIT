"""
This module defines api views

"""
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.helpers.token_required import token_required
from api.model.black_list_tokens import BlackListTokens
from api.model.orders import Orders



class FilterOrders(MethodView):
    """Class to define all the api end points"""
    @token_required
    def post(self, current_user):
        """method to filter out orders"""
        user_role = current_user[0][7]
        if user_role == 'admin':
            search_term = (request.get_json())["search_term"]
            return Orders.execute_query_to_filter_out_orders(
                self,search_term
            ) 
        return jsonify({'message':'Cannot Perform That Function!'}), 404
       
