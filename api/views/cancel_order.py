"""
This module defines api end point to enable an user to cancel an orer

"""
from flask import jsonify
from flask import request
from flask.views import MethodView
from api.model.orders import Orders
from api.helpers.token_required import token_required

class CancelOrder(MethodView):
    """Class to define an endpoint to update a specific user order status"""
    @token_required
    def put(self,current_user, parcel_id):
        """function to enable an a user to cancel a specific order"""
        user_role = current_user[0][7]
        user_id = current_user[0][0]
        #check if user is admin
        if user_role == 'user':
            try:
                parcel_id = int(parcel_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            if request.json['order_status'] != 'delivered':
                return Orders.cancel_a_parcel_order(self, parcel_id, user_id, 
                request.json['order_status'])
            return jsonify({'message':'You are only allowed to cancel an order'}), 406 
        return jsonify({'message':'You Cannot Perform That Function!'}), 404

    
