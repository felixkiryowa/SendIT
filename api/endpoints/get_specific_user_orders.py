"""
This module defines api views

"""
import datetime
from flask import jsonify, request
from flask.views import MethodView
from api.endpoints.orders import OrdersApi, Order_object
from api.validators.validate import check_if_no_user_orders

class UserSpecificOrders(MethodView):
    """Class to define an endpoint to get a specific user order"""
    orders_object = OrdersApi()
    orders_list = orders_object.orders
 
    def get(self, user_id):
        """function to get a single order for a user"""
        if isinstance(user_id, int):
            user_specific_orders = Order_object.select_specific_order('user_id', user_id)
            return check_if_no_user_orders(user_specific_orders, user_id)
        raise ValueError('The user Id must be an integer')