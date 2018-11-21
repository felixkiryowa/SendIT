"""
This module defines api end point to enable an admin to update the order status

"""
from flask import jsonify
from flask import request
from flask.views import MethodView
from api.model.orders import Orders
from api.token.token_required import token_required

class UpdateOrderPresentLocation(MethodView):
    """Class to define an endpoint to update a specific user order status"""
    @token_required
    def put(self,current_user, parcel_id):
        """function to enable an admin to change the status of a specific order"""
        user_role = current_user[0][7]
        #check if user is admin
        if user_role == 'admin':
            try:
                parcel_id = int(parcel_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            return Orders.update_order_location(self, parcel_id,
            request.json['location'])
        return jsonify({'message':'Cannot Perform That Function!'}), 404

    
