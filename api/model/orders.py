"""This is orders class defining the orders class model constructor """
from api import connection
from flask import jsonify

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
            order_name VARCHAR(100) NOT NULL,
            parcel_weight INTEGER NOT NULL,
            price BIGINT NOT NULL,
            parcel_pickup_address VARCHAR(100) NOT NULL,
            parcel_destination_address VARCHAR(100) NOT NULL,
            order_status VARCHAR(100)  DEFAULT 'pending',
            receivers_names VARCHAR(100) NOT NULL,
            receivers_contact VARCHAR(100) NOT NULL,
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
        self.order_name = args[1]
        self.parcel_weight = args[2]
        self.price = args[3]
        self.parcel_pickup_address = args[4]
        self.parcel_destination_address = args[5]
        self.receivers_names = args[6]
        self.receivers_contact = args[7]
        self.location = args[8]
        
    
    
    def execute_add_order_query(self):
        """
        method to excute query to add a new order to the database
        """
        sql = """INSERT INTO orders(senders_user_id,order_name,parcel_weight,price,parcel_pickup_address,
        parcel_destination_address,receivers_names,receivers_contact,location)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING parcel_order_id;"""
        # create a new cursorsor
        cursor = connection.cursor()
        # execute the INSERT statement
        cursor.execute(sql, (self.senders_user_id, self.order_name, self.parcel_weight, self.price, 
        self.parcel_pickup_address, self.parcel_destination_address, self.receivers_names, 
        self.receivers_contact,self.location))
        # commit the changes to the database
        connection.commit()

    @staticmethod
    def execute_query_get_all_orders(self):
        """
        method to query for all orders in the database
        """
        orders =  """
            SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
            orders.receivers_names,orders.receivers_contact,orders.created_at,
            orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
            FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id ORDER BY orders.parcel_order_id;
        """
        cursor = connection.cursor()
        cursor.execute(orders)
        orders_data = cursor.fetchall()
        if not orders_data:
            return jsonify({"Message":"No Order Entries Found !!"}), 200
        columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
        'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
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
            SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
            orders.receivers_names,orders.receivers_contact,orders.created_at,
            orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
            FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s
            ORDER BY orders.parcel_order_id;
        """
        cursor = connection.cursor()
        cursor.execute(order,(order_id, ))
        order_data = cursor.fetchall()
        if not order_data:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
        'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
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
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        cursor.execute("UPDATE orders SET parcel_destination_address=%s WHERE parcel_order_id=%s",(order_destination, order_id,))
        connection.commit()
        return  Orders.execute_query_get_specific_order(self, order_id)

    @staticmethod
    def update_order_status(self, order_id, order_status):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(order_id, ))
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        cursor.execute("UPDATE orders SET order_status=%s WHERE parcel_order_id=%s",(order_status, order_id,))
        connection.commit()
        return  Orders.execute_query_get_specific_order(self, order_id)

    @staticmethod
    def update_order_location(self, order_id, order_location):
        """
        method to update the current location of a specific order
        """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(order_id, ))
        order_data = cursor.rowcount
        if order_data == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)}), 404
        cursor.execute("UPDATE orders SET location=%s WHERE parcel_order_id=%s",(order_location, order_id,))
        connection.commit()
        return  Orders.execute_query_get_specific_order(self, order_id)

    @staticmethod
    def  get_specific_user_orders(self, user_id):
        """
        method to get a specific user orders from the database
        """
        orders_query =  """
                SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.senders_user_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders WHERE senders_user_id =%s",(user_id, ))
        user_exist = cursor.rowcount
        if user_exist == 0:
            return jsonify({"Message":"No Orders Found For User With A User Id Of "+ str(user_id)}), 404
        cursor.execute(orders_query, (user_id,))
        all_user_orders_data = cursor.fetchall()
        connection.commit()
        columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
            'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
        results = []
        for row in all_user_orders_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'Specific_order':results}), 200 
        
        
