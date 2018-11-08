"""
This module defines api views

"""
import datetime
from flask import jsonify, request
from flask.views import MethodView
from api.endpoints.orders import OrdersApi


class UserSpecificOrders(MethodView):
    """Class to define an endpoint to get a specific user order"""
    orders_object = OrdersApi()
    orders_list = orders_object.orders
 
    def get(self, user_id):
        """function to get a single order for a user"""
        user_specific_orders = [
            order.__dict__ for order in self.orders_list
            if order.__dict__["user_id"] == user_id
        ]
        return jsonify({'order':user_specific_orders})
