"""
This module defines api end point to enable an admin to update the order status

"""
from flask import jsonify
from flask import request
from flask.views import MethodView
from api.model.orders import Orders
from api.helpers.token_required import token_required

class UserSpecificOrder(MethodView):
    """Class to define an endpoint to get a specific user order"""
    # orders_object = OrdersApi()
    # orders_list = orders_object.orders
    @token_required
    def get(self, current_user, parcel_id):
        """function to get a single order for a user"""
        print(parcel_id)
        user_role = current_user[0][7]
        specific_user_id = current_user[0][0]
        if user_role == 'user':
            try:
                user_id = int(specific_user_id)
                order_parcel_id = int(parcel_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            return Orders.get_single_user_order(self, user_id, order_parcel_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404


    
