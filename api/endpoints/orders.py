"""
This module defines api views

"""
import datetime
from flask import jsonify, request
from flask.views import MethodView
from api.model.orders import Orders


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
            return jsonify({'all orders':[order.__dict__ for order in self.orders]})
        specific_order = [
            order.__dict__ for order in self.orders
            if order.__dict__["order_id"] == order_id
        ]
        return jsonify({'order':specific_order[0]})
   
    def post(self):
        """funtion to place a new order"""
        get_todays_date = datetime.datetime.now()
        print(get_todays_date)
        price_to_be_paid = request.json['parcel_weight'] * 30000
        order = Orders(
            request.json['user_id'], len(self.orders) + 1, request.json['order_name'],
            request.json['senders_names'], request.json['senders_contact'], 
            request.json['parcel_pickup_address'], request.json['parcel_destination_address'], 
            request.json['receivers_names'], request.json['receivers_contact'], 
            request.json['parcel_weight'], price_to_be_paid, get_todays_date, request.json['order_status']
        )
        self.orders.append(order)
        return jsonify(order.__dict__)

    def put(self, parcel_id):
        order = [order.__dict__ for order in self.orders if order.__dict__['order_id'] == parcel_id]
        if not order: 
            for order in self.orders:
                if order.__dict__["order_id"] == parcel_id:
                    order.__dict__['order_status'] = request.json['order_status']
            return jsonify({'orders':[order.__dict__ for order in self.orders]})
        return jsonify({'Message':'No Order Found with Specified Route Parameter'})
           