"""
This module defines api views

"""
from flask import jsonify, request
from flask import json
from flask import Response
from flask.views import MethodView
from api.model.orders import Orders
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
        #Here is the logic to get all orders and single order
        get_single_order_sql =  """
                    SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                    orders.receivers_names,orders.receivers_contact,orders.created_at,
                    orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                    FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s
                    ORDER BY orders.parcel_order_id;
                """
        
        get_all_orders_sql =  """
                    SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                    orders.receivers_names,orders.receivers_contact,orders.created_at,
                    orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                    FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id ORDER BY orders.parcel_order_id;
                """
        user_type = current_user[0][7]
        #check if user is admin
        if user_type == 'admin':
            if parcel_order_id is None:
                return Orders.execute_query_get_all_orders(self,get_all_orders_sql)
            try:
                order_id = int(parcel_order_id)
            except:
                return jsonify({'message':'Invalid Parcel Id'}), 400
            return  Orders.execute_query_get_specific_order(self, get_single_order_sql,order_id)
        return jsonify({'message':'Cannot Perform That Function!'}), 404
  

    @token_required
    def post(self, current_user):
        """funtion to place a new order"""
        new_parcel_order = request.get_json()
        price = new_parcel_order['parcel_weight'] * 50000
        parcel_location = new_parcel_order['parcel_pickup_address']
        user_id = current_user[0][0]
        return ORDER_OBJECT.validate_posted_data(new_parcel_order, user_id, price, parcel_location)

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
