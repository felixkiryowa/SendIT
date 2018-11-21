"""
This module defines api views

"""
import re
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.token.token_required import token_required
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
        parcel_order = request.get_json()
        return ORDER_OBJECT.validate_posted_data(current_user, parcel_order)
    def check_posted_user_object_for_keys(self, new_user):
        """
        method to check for keys in a user posted order object
        """
        order_keys = [
            'order_name', 'parcel_weight',
            'parcel_pickup_address',
            'parcel_destination_address',
            'receivers_names', 'receivers_contact'
        ]
        if set(order_keys).issubset(new_user):
            return True
        return False

    def validate_parcel_weight_is_an_integer(self, parcel_order):
        """
        method to check whether parcel weight is an integer
        """
        if(isinstance(parcel_order['parcel_weight'], int)):
            return True
        return False

    def  validate_posted_data_for_empty_strings(self, parcel_order):
        """
        method to validate posted order for empty strings
        """
        if (parcel_order['order_name'] != '' and
            parcel_order['parcel_pickup_address']
            and parcel_order['parcel_destination_address'] != '' and parcel_order['receivers_names']
            and parcel_order['receivers_contact'] != ''
        ):
            return True
        return False

    def search_regular_expression_characters(self, parcel_order):
        """
        method to search for regular expressions in posted order data
        """
        #create a regular expression object to be used in matching
        regex = re.compile(r'[@_!#$%^&*()<>?/\|}{~:]') 
        #check if a posted order data contails regular expressions
        if (regex.search(parcel_order['order_name']) is None and regex.search(parcel_order['parcel_pickup_address']) is None 
        and regex.search(parcel_order['parcel_destination_address']) is None and regex.search(parcel_order['receivers_names']) is None
        and regex.search(parcel_order['receivers_contact']) is None):       
            return True  
        return False 

    def validate_phone_number_consist_of_digits(self, parcel_order):
        """
        method to check whether a phone number consist of only digits
        """
        if(parcel_order['receivers_contact'].isdigit() and len(parcel_order['receivers_contact']) == 10):
            return True
        return False

        

    def validate_posted_data(self, current_user, parcel_order):
        """
        method to validate user posted order object
        """
        if (self.check_posted_user_object_for_keys(parcel_order) and 
        self.validate_parcel_weight_is_an_integer(parcel_order) and 
        self.validate_posted_data_for_empty_strings(parcel_order) and 
        self.search_regular_expression_characters(parcel_order) and 
        self.validate_phone_number_consist_of_digits(parcel_order)):
            price = parcel_order['parcel_weight'] * 50000
            parcel_location = parcel_order['parcel_pickup_address']
            user_id = current_user[0][0]
            Orders(user_id, parcel_order['order_name'], parcel_order['parcel_weight'], 
            price, parcel_order['parcel_pickup_address'], 
            parcel_order['parcel_destination_address'], parcel_order['receivers_names'], 
            parcel_order['receivers_contact'], parcel_location).execute_add_order_query()
            return jsonify({'message':'Successfully created an order'}), 201
        parcel_order_object = "{'order_name': 'phones','parcel_weight': 6,'parcel_pickup_address': 'Kamwokya','parcel_destination_address': 'Mpigi',\
        'receivers_contact': '070786543','receivers_names': 'Mukasa Derrick'}"
        bad_order_object = {
        "Invalid_order_object":parcel_order_object
        }
        response = Response(
            json.dumps(bad_order_object),
            status=400, mimetype="application/json"
            )
        return response


#create an object of the class
ORDER_OBJECT = OrdersApi()
