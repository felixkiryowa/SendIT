"""
This module defines api views

"""
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.token.token_required import token_required
from api.validators.validate import check_empty_list
from api.validators.validate import  check_if_there_no_orders
from api.validators.validate import  check_if_posted_order_status_is_string
from api.validators.validate import  check_if_posted_order_status_is_not_empty_string
from api.validators.validate import check_order_object_keys
from api.model.orders import Orders



class OrdersApi(MethodView):
    """Class to define all the api end points"""

    
    @token_required
    def get(self, current_user, parcel_order_id):
        """function to get a single order or to get all the orders"""
        user_role = current_user[0][7]
        #check if user is admin
        if user_role == 'admin':
            if parcel_order_id is None:
                return Orders.execute_query_get_all_orders(self)
            try:
                order_id = int(parcel_order_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            return  Orders.execute_query_get_specific_order(self, order_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404
  

    @token_required
    def post(self, current_user):
        """funtion to place a new order"""
        new_parcel_order = request.get_json()
        price = new_parcel_order['parcel_weight'] * 50000
        parcel_location = new_parcel_order['parcel_pickup_address']
        user_id = current_user[0][0]
        return ORDER_OBJECT.validate_posted_data(new_parcel_order, user_id, price, parcel_location)

    def validate_posted_data(self, new_parcel_order, user_id, price, parcel_location):
        """
        function to validate user posted order object
        """
        if (check_order_object_keys(new_parcel_order)) == True:
            Orders(user_id, new_parcel_order['order_name'], new_parcel_order['parcel_weight'], 
            price, new_parcel_order['parcel_pickup_address'], 
            new_parcel_order['parcel_destination_address'], new_parcel_order['receivers_names'], 
            new_parcel_order['receivers_contact'], parcel_location).execute_add_order_query()
            return jsonify({'message':'Successfully created an order'}), 201
        parcel_order_object = "{'order_name': 'phones','parcel_weight': 6,'parcel_pickup_address': 'Kamwokya','parcel_destination_address': 'Mpigi',\
        'receivers_contact': '070786543','receivers_names': 'Mukasa Derrick'}"
        bad_order_object = {
        "Invalid_user_object":parcel_order_object
        }
        response = Response(
            json.dumps(bad_order_object),
            status=400, mimetype="application/json"
            )
        return response

#create an object of the class
ORDER_OBJECT = OrdersApi()
