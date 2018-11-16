"""
This module defines api end point to enable an admin to update the order status

"""
from flask import jsonify
from flask.views import MethodView
from api.endpoints.orders import OrdersApi, ORDER_OBJECT
from api.token.token_required import token_required
from api.validators.validate import check_if_no_user_orders

class UserSpecificOrders(MethodView):
    """Class to define an endpoint to get a specific user order"""
    orders_object = OrdersApi()
    orders_list = orders_object.orders
    @token_required
    def get(self, current_user, specific_user_id):
        """function to get a single order for a user"""
        try:
            user_id = int(specific_user_id)
        except:
            return jsonify({'message':'Invalid User Id'}), 400
        user_specific_orders = ORDER_OBJECT.select_specific_order('user_id', user_id)
        return check_if_no_user_orders(user_specific_orders, user_id)
