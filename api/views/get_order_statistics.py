"""
This module defines api views

"""
import re
from flasgger import swag_from
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.helpers.token_required import token_required
from api.model.orders import Orders



class OrdersStatistics(MethodView):
    """Class to define all the api end points"""
    @swag_from('../docs/orders.yml')
    @token_required
    def get(self, current_user):
        """function to get a single order or to get all the orders"""
        user_role = current_user[0][7]
        #check if user is admin
        if user_role == 'admin':
            return  Orders.execute_query_get_order_statistics(self)
        return jsonify({'message':'Cannot Perform That Function!'}), 404
