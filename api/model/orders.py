"""This is orders class defining the orders class model constructor """
import psycopg2
from api import connection
from flask import jsonify
from flask_mail import Message
from api import mail


cursor = connection.cursor()

class Orders:
    """
    Class to define the attributes of a parcel order
    """

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            parcel_order_id SERIAL PRIMARY KEY,
            senders_user_id INTEGER NOT NULL,
            order_name VARCHAR(100) NULL,
            parcel_weight INTEGER NOT NULL,
            price BIGINT NOT NULL,
            parcel_pickup_address VARCHAR(100) NOT NULL,
            parcel_destination_address VARCHAR(100) NOT NULL,
            order_status VARCHAR(100)  DEFAULT 'pending',
            receivers_names VARCHAR(100)  NULL,
            receivers_contact VARCHAR(100)  NULL,
            created_at TIMESTAMP DEFAULT NOW(),
            ordering_time TIME DEFAULT NOW(),
            location VARCHAR(100) NOT NULL,
            FOREIGN KEY (senders_user_id)
                REFERENCES users(user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """
    )
    
    def __init__(self, *args):
        """This is orders class constructor"""
        self.senders_user_id = args[0]
        self.parcel_weight = args[1]
        self.price = args[2]
        self.parcel_pickup_address = args[3]
        self.parcel_destination_address = args[4]
        self.location = args[5]
        
    
    
    def execute_add_order_query(self):
        """
        method to excute query to add a new order to the database
        """
        sql = """INSERT INTO orders(senders_user_id,parcel_weight,price,parcel_pickup_address,
        parcel_destination_address,location)
                VALUES(%s,%s,%s,%s,%s,%s) RETURNING parcel_order_id;"""
        # create a new cursorsor
        cursor = connection.cursor()
        # execute the INSERT statement
        cursor.execute(sql, (self.senders_user_id, self.parcel_weight, self.price, 
        self.parcel_pickup_address, self.parcel_destination_address,
        self.location))
        # commit the changes to the database
        connection.commit()

    @staticmethod
    def execute_query_get_all_orders(self):
        """
        method to query for all orders in the database
        """
        orders =  """

        SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.location,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id  WHERE orders.order_status=%s AND NOT orders.order_status=%s AND NOT orders.order_status=%s ORDER BY orders.parcel_order_id;
        """
        cursor = connection.cursor()
        cursor.execute(orders,('pending','delivered','cancelled',))
        orders_data = cursor.fetchall()
        if not orders_data:
            return jsonify({"message":"No Order Entries Found !!"}), 200
        columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
            'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders firstname','senders lastname','senders phone contact')
        results = []
        for row in orders_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'All_orders':results})

    @staticmethod 
    def execute_query_get_specific_order(self, order_id):
        """
        method to query a single specific order from the database
        """
        order =  """

         SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.location,users.first_name,users.last_name,users.phone_contact,users.email
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s ORDER BY orders.parcel_order_id;
        """
        cursor = connection.cursor()
        cursor.execute(order,(order_id, ))
        order_data = cursor.fetchall()
        if not order_data:
            return jsonify({"message":"No Order Found With That Order Id"}), 404
        columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
            'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders_firstname','senders_lastname','senders_phonecontact','senders_email')
        results = []
        for row in order_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'Specific_order':results}), 200 

    @staticmethod 
    def execute_query_to_filter_out_orders(self,search_term):
        """
        method to filter out orders from the database
        """
        order =  """
        SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,
        orders.parcel_destination_address,
        orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
        orders.location,users.first_name,users.last_name,users.phone_contact,users.email
        FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE  orders.order_name ILIKE '%%' || %s || '%%'
        OR orders.parcel_pickup_address ILIKE '%%' || %s || '%%' OR orders.parcel_destination_address ILIKE '%%' || %s || '%%' 
        OR orders.receivers_names ILIKE '%%' || %s || '%%' OR orders.receivers_contact ILIKE '%%' || %s || '%%';
        """
        cursor = connection.cursor()
        cursor.execute(order,(search_term, search_term, search_term, search_term, search_term, ))
        order_data = cursor.fetchall()
        if not order_data:
            return jsonify({"message":"No Orders Found"}), 404
        columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
            'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders_firstname','senders_lastname','senders_phonecontact','senders_email')
        results = []
        for row in order_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'Specific_order':results}), 200 
        

    
    @staticmethod
    def update_order_destination(self, order_id, order_destination, user_id):
        """
        method to update the parcel order current location
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s and senders_user_id =%s",(order_id, user_id, ))
        current_order = cursor.fetchall()
        current_order_status = current_order[0][7]
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        elif current_order_status != 'delivered' and current_order_status != 'cancelled':
            cursor.execute("UPDATE orders SET parcel_destination_address=%s WHERE parcel_order_id=%s",(order_destination, order_id,))
            connection.commit()
            # return  Orders.execute_query_get_specific_order(self, order_id)
            return jsonify({'message':'You Have Successfully Updated The Parcel Delivery Order Destination'});
        return jsonify({'message':'The order is ' + current_order_status + ' already so its destination cannot be updated'}), 406
        

    @staticmethod
    def update_order_status(self, order_id, order_status):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(order_id, ))
        order = cursor.fetchall()
        current_order_status = order[0][7]
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        elif order_status == 'delivered' and current_order_status == 'pending':
            cursor.execute("UPDATE orders SET order_status=%s WHERE parcel_order_id=%s",(order_status, order_id,))
            connection.commit()
            return  Orders.execute_query_get_specific_order(self, order_id)
        return jsonify({'message':'The parcel order  is already '+current_order_status}), 406

    @staticmethod
    def update_order_location(self, order_id, order_location):
        """
        method to update the current location of a specific order
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(order_id, ))
        current_order = cursor.fetchall()
        current_order_status = current_order[0][7]
        current_order_name = current_order[0][2]
        order_owner_id = current_order[0][1]
        cursor.execute("SELECT * FROM users WHERE user_id=%s",(order_owner_id, ))
        current_user = cursor.fetchall()
        owner_email = current_user[0][3]
        print(owner_email)
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        elif current_order_status != 'delivered' and current_order_status != 'cancelled':
            msg = Message(current_order_name + "  Order Notification",
                  sender="fkiryowa@nwt.ug",
                  recipients=[owner_email])
            msg.body = "The current location of your parcel order is " + order_location
            # mail.send(msg)
            cursor.execute("UPDATE orders SET location=%s WHERE parcel_order_id=%s",(order_location, order_id,))
            connection.commit()
            mail.send(msg)
            return  Orders.execute_query_get_specific_order(self, order_id)
        return jsonify({'message':'The order is ' + current_order_status + ' already'}), 406

    @staticmethod
    def cancel_a_parcel_order(self, parcel_id, user_id, order_status):
        """
        method to enable a user to cancel an order
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s AND senders_user_id=%s",(parcel_id, user_id,  ))
        current_order = cursor.fetchall()
        if current_order:
            current_order_status = current_order[0][7]
            order_data = cursor.rowcount
            if order_data == 0:
                return jsonify({"message":"No Order Found With Order Id Of "+ str(parcel_id)}), 404
            elif current_order_status != 'delivered' and current_order_status != 'cancelled':
                cursor.execute("UPDATE orders SET order_status=%s WHERE parcel_order_id=%s",(order_status, parcel_id,))
                connection.commit()
                # return  Orders.execute_query_get_specific_order(self, parcel_id)
                return jsonify({'message':'You Have Successfully Cancelled The Parcel Delivery Order'});
            return jsonify({'message':'The order is ' + current_order_status + ' already'}), 406
        return jsonify({'message':'Your Not The Owner Of That Parcel Order ,You Cant Change its status'}), 406
    

    @staticmethod
    def  get_specific_user_orders(self, user_id):
        """
        method to get a specific user orders from the database
        """
        orders_query =  """
                SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.location,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.senders_user_id=%s AND NOT orders.order_status=%s AND NOT orders.order_status=%s
                ORDER BY orders.parcel_order_id;
            """
        order_status = "cancelled"
        delivered = "delivered"
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE senders_user_id =%s",(user_id, ))
        user_exist = cursor.rowcount
        if user_exist == 0:
            return jsonify({"message":"No Orders Found, You Can Make An Order Now!!!"}), 404
        cursor.execute(orders_query, (user_id, order_status,delivered,))
        existing_orders = cursor.rowcount
        if existing_orders != 0:
            all_user_orders_data = cursor.fetchall()
            connection.commit()
            columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
            'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders firstname','senders lastname','senders phone contact')
            results = []
            for row in all_user_orders_data:
                results.append(dict(zip(columns, row)))
            return jsonify(results), 200 
        return jsonify({"message":"No Orders Found, You Can Make An Order Now!!!"}), 404


    @staticmethod
    def get_user_delivered_orders(self, user_id):
        """
        method to get a specific user delivered orders from the database
        """
        orders_query =  """
                SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.location,users.first_name,users.last_name,users.phone_contact,users.email
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.senders_user_id=%s AND orders.order_status=%s
                ORDER BY orders.parcel_order_id;
            """
        delivered = "delivered"
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE senders_user_id =%s",(user_id, ))
        user_exist = cursor.rowcount
        if user_exist == 0:
            return jsonify({"message":"No Orders Found, You Can Make An Order Now!!!"}), 404
        cursor.execute(orders_query, (user_id, delivered,))
        existing_orders = cursor.rowcount
        if existing_orders != 0:
            all_user_orders_data = cursor.fetchall()
            connection.commit()
            columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
            'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders_firstname','senders_lastname','senders_phone_contact', 'senders_email')
            results = []
            for row in all_user_orders_data:
                results.append(dict(zip(columns, row)))
            return jsonify({'Specific_order':results}), 200 
        return jsonify({"message":"No Orders Found, You Can Make An Order Now!!!"}), 404



    @staticmethod
    def  get_single_user_order(self, user_id, order_parcel_id):
        """
        method to get a specific user order from the database
        """
        orders_query =  """
                SELECT orders.parcel_order_id,orders.senders_user_id,orders.order_name,orders.parcel_weight,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.order_status,orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.location,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.senders_user_id=%s AND orders.parcel_order_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE senders_user_id =%s AND parcel_order_id=%s",(user_id,order_parcel_id, ))
        user_exist = cursor.rowcount
        if user_exist == 0:
            return jsonify({"message":"No Orders Found, Make An Order"}), 404
        cursor.execute(orders_query, (user_id,order_parcel_id,))
        all_user_orders_data = cursor.fetchall()
        connection.commit()
        columns = ('parcel_order_id','senders_user_id','order_name','parcel_weight','price','parcel_pickup_address','parcel_destination_address',
        'order_status','receivers_names','receivers_contact','created_at','order_current_location','senders firstname','senders lastname','senders phone contact')
        results = []
        for row in all_user_orders_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'order':results}), 200 


    def execute_query_get_order_statistics(self):
        """
        method to get order statistics
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_status =%s",('pending', ))
        pending = cursor.rowcount
        cursor.execute("SELECT * FROM orders WHERE order_status =%s",('delivered', ))
        delivered = cursor.rowcount
        cursor.execute("SELECT * FROM orders WHERE order_status =%s",('cancelled', ))
        cancelled = cursor.rowcount
        Orders_statistics = {
            "pending":pending,
            "delivered":delivered,
            "cancelled":cancelled
        }
        return jsonify({"message":Orders_statistics})

        
        
