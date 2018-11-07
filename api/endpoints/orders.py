"""
This module defines api views

"""
from flask import jsonify
from flask.views import MethodView
from api.model.orders import Orders

class OrdersApi(MethodView):
    """Class to define all the api end points"""
    order1 = Orders(
        1, 1, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018"
    )
    order2 = Orders(
        1, 1, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018"
    )
    order3 = Orders(
        1, 1, "pizza", "esther nakiganda", "0700978654", "Lubaga", "Ntinda", "kakembo adam",
        "079234567", 4, 40000, "22/10/2018"
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
