import datetime
from flask import jsonify, request, json
from api.model.orders import Orders
from validate_email import validate_email
# is_valid = validate_email('example@example.com')


def check_empty_list(check_list, order_id):
    """
    function to check whether a list is empty
    """
    if not check_list:
        return jsonify({'message':'No Order Found with specified Id ' + str(order_id)}),200
    return jsonify({'order':check_list[0]}),200

def  check_if_no_user_orders(order_list, user_id):
    """
    function to check whether there are orders for a specific user
    """
    if not order_list:
        message = 'No Order Found with specified Id  ' + str(user_id)
        return jsonify({'message':message}),200
    return jsonify({'order':order_list[0]}),200



def check_if_there_no_orders(all_orders_list):
    """
    function to check if there are no orders
    """
    if not all_orders_list:
        return jsonify({'message':'No Orders Found!!!'}),200
    return jsonify({'all orders':[order.__dict__ for order in all_orders_list]}),200
    

def validate_posted_data(posted_order, orders_list):
    """
    function to validate user posted order object
    """
    if ('user_id' in posted_order and 'order_name' in posted_order and
        'senders_names' in posted_order and 'senders_contact' in posted_order and
        'parcel_pickup_address' in posted_order and 'parcel_destination_address' in posted_order and
        'receivers_names' in posted_order and 'receivers_contact' in posted_order and
        'parcel_weight' in posted_order
    ):

        get_todays_date = datetime.datetime.now()
        order_status = 'pending'
        price_to_be_paid = request.json['parcel_weight'] * 30000
        order = Orders(
            request.json['user_id'], len(orders_list) + 1, request.json['order_name'],
            request.json['senders_names'], request.json['senders_contact'], 
            request.json['parcel_pickup_address'], request.json['parcel_destination_address'], 
            request.json['receivers_names'], request.json['receivers_contact'], 
            request.json['parcel_weight'], price_to_be_paid, get_todays_date, order_status
        )
        orders_list.append(order)
        return jsonify(order.__dict__),201
    parcel_order_object = "{'item_name': 'Greens','price':50000,'current_items':40}"
    bad_order_object = {
    "error": "Bad Order Object",
    "help of the correct order object format":parcel_order_object
    }
    response = Response(
        json.dumps(bad_order_object),
        status=400, mimetype="application/json"
        )
    return response