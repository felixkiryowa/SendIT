"""
This module defines api views

"""
import datetime
from flask import jsonify, request, Response , json
from flask.views import MethodView
from api.model.orders import Orders
from api.validators.validate import check_empty_list, check_if_there_no_orders, validate_posted_data


class OrdersApi(MethodView):
    """Class to define all the api end points"""
    order1 = Orders(
        1, 1, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018", "received"
    )
    order2 = Orders(
        1, 2, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018", "received"
    )
    order3 = Orders(
        1, 3, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018", "received"
    )

    orders = [order1, order2, order3]

    

    def get(self, order_id):
        """function to get a single order or to get all the orders"""
        if order_id is None:
            # return a list of orders
            return check_if_there_no_orders(self.orders)
        if not isinstance(order_id,(float,bool,str,list,tuple)):
            specific_order = Order_object.select_specific_order('order_id', order_id)
            return check_empty_list(specific_order, order_id)
        raise ValueError('The order Id must be an int')
   
    def post(self):
        """funtion to place a new order"""
        new_parcel_order = request.get_json()
        return validate_posted_data(new_parcel_order, self.orders)

    def put(self, parcel_id):
        """function to update the order status"""
        order = Order_object.select_specific_order('order_id', parcel_id)
        if  order:
            return Order_object.update_specidfic_order_status_logic(order, parcel_id)   
        return jsonify({'Message':'No Order Found with Specified Route Parameter'}),404
        
  
    def select_specific_order(self, access_key , specific_id):
        """function to do logic of selecting a specific order using order_id or user_id"""
        if isinstance(access_key, str) and isinstance(specific_id, int):
            return [order.__dict__ for order in self.orders if order.__dict__[access_key] == specific_id]
        raise ValueError('The parameter passed should be an int and access key a string')

    def update_specidfic_order_status_logic(self, order, parcel_id):
        for order in self.orders:
            if order.__dict__["order_id"] == parcel_id:
                order.__dict__['order_status'] = request.json['order_status']
        return jsonify({'orders':[order.__dict__ for order in self.orders]}),200

# create an object of the class
Order_object = OrdersApi()