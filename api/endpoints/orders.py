"""
This module defines api views

"""
from flask import jsonify, request
from flask.views import MethodView
from api.model.orders import Orders
from api.token.token_required import token_required
from api.validators.validate import check_empty_list
from api.validators.validate import  check_if_there_no_orders
from api.validators.validate import  validate_posted_data
from api.validators.validate import  check_if_posted_order_status_is_string
from api.validators.validate import  check_if_posted_order_status_is_not_empty_string


class OrdersApi(MethodView):
    """Class to define all the api end points"""
    orders = []

    @token_required
    def get(self, current_user, parcel_order_id):
        """function to get a single order or to get all the orders"""
        user_type = current_user.__dict__['user_type']
        #check if user is admin
        if user_type == 'admin':
            if parcel_order_id is None:
                # return a list of orders
                return check_if_there_no_orders(self.orders)
            try:
                order_id = int(parcel_order_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            specific_order = ORDER_OBJECT.select_specific_order('order_id', order_id)
            return check_empty_list(specific_order, order_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404
    @token_required
    def post(self, current_user):
        """funtion to place a new order"""
        new_parcel_order = request.get_json()
        user_id = current_user.__dict__['user_id']
        return validate_posted_data(new_parcel_order, self.orders, user_id)

    @token_required
    def put(self, current_user, order_parcel_id):
        """function to update the order status"""
        try:
            parcel_id = int(order_parcel_id)
        except:
            return jsonify({'message':'Invalid Parcel Id'}), 400
        user_type = current_user.__dict__['user_type']
        order = ORDER_OBJECT.select_specific_order('order_id', parcel_id)
        get_order_status = ORDER_OBJECT.check_order_status_of_an_order(
            'order_status', 'delivered', 'order_id', parcel_id
        )
        return ORDER_OBJECT.check_user_type_logic(user_type, get_order_status, order,parcel_id)
        

    def select_specific_order(self, access_key, specific_id):
        """function to do logic of selecting a specific order using order_id or user_id"""
        if isinstance(access_key, str) and isinstance(specific_id, int):
            return [
                order.__dict__ for order in self.orders if order.__dict__[access_key] == specific_id
            ]
        raise ValueError(
            'The parameter passed should be an int and access key a string'
        )

    def check_order_status_of_an_order(self, access_key, order_status, access_key_parcel_id, specific_id):
        """
        function to check the order status of an order to allow whether a user should
        update it or not
        """
        return [
                order.__dict__ for order in self.orders 
                if order.__dict__[access_key_parcel_id] == specific_id
                and order.__dict__[access_key] == order_status
        ] 
    def update_specific_order_status_logic(self, order, parcel_id):
        """
        function to handle updating order status logic
        """
        if(check_if_posted_order_status_is_string() and 
            check_if_posted_order_status_is_not_empty_string):
            return ORDER_OBJECT.refactor_update_specific_order_logic(order, parcel_id)
        return jsonify({'message':'The status order can only be a string'})

    def check_user_type_logic(self, user_type, get_order_status, order,parcel_id):
        if  user_type == "user":
            if not get_order_status:
               return ORDER_OBJECT.refactor_check_user_type_logic(order, parcel_id)
            return jsonify(
                {'message':'The Order has already been delivered so it cant be cancelled'}
            )
        return jsonify({'message':'Cannot Perform That Function!'}), 401

    def refactor_update_specific_order_logic(self, order, parcel_id ):
        for order in self.orders:
            if order.__dict__["order_id"] == parcel_id:
                order.__dict__['order_status'] = request.json['order_status']
        return jsonify({'orders':[order.__dict__ for order in self.orders]}), 200

    def refactor_check_user_type_logic(self, order, parcel_id):
        if  order:
            return ORDER_OBJECT.update_specific_order_status_logic(order, parcel_id)
        return jsonify({'message':'No Order Found with Specified Route Parameter'}), 404

# create an object of the class
ORDER_OBJECT = OrdersApi()
