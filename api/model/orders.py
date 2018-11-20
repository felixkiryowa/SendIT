"""This is orders class defining the orders class model constructor """
from api import conn
from flask import jsonify

cur = conn.cursor()

class Orders:
    """
    Class to define the attributes of a parcel order
    """

    cur.execute(
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
        sql = """INSERT INTO orders(senders_user_id,order_name,parcel_weight,price,parcel_pickup_address,
        parcel_destination_address,receivers_names,receivers_contact,location)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING parcel_order_id;"""
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (self.senders_user_id, self.order_name, self.parcel_weight, self.price, 
        self.parcel_pickup_address, self.parcel_destination_address, self.receivers_names, 
        self.receivers_contact,self.location))
        # commit the changes to the database
        conn.commit()

    @staticmethod
    def execute_query_get_all_orders(self,sql):
        cur = conn.cursor()
        cur.execute(sql)
        returned_orders_data = cur.fetchall()
        if not returned_orders_data:
            return jsonify({"Message":"No Order Entries Found !!"}), 200
        columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
        'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
        results = []
        for row in returned_orders_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'All_orders':results})

    @staticmethod 
    def execute_query_get_specific_order(self, sql, order_id):
            cur = conn.cursor()
            cur.execute(sql,(order_id, ))
            specific_order_data = cur.fetchall()
            if not specific_order_data:
                return jsonify({"Message":"No Order Found With Order Id Of "+ str(order_id)})
            columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
            'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
            results = []
            for row in specific_order_data:
                results.append(dict(zip(columns, row)))
            return jsonify({'Specific_order':results}), 200 

    
    @staticmethod
    def update_order_destination(self, parcel_order_id, new_order_destination, user_id):
        get_single_order_sql =  """
                SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE parcel_order_id=%s and senders_user_id =%s",(parcel_order_id, user_id, ))
        check_order_exist = cur.rowcount
        if check_order_exist == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(parcel_order_id)}), 200
        cur.execute("UPDATE orders SET parcel_destination_address=%s WHERE parcel_order_id=%s",(new_order_destination, parcel_order_id,))
        conn.commit()
        return  Orders.execute_query_get_specific_order(self,get_single_order_sql,parcel_order_id)

    @staticmethod
    def update_order_status(self, parcel_order_id, new_order_status):
        get_single_order_sql =  """
                SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(parcel_order_id, ))
        check_order_exist = cur.rowcount
        if check_order_exist == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(parcel_order_id)}), 200
        cur.execute("UPDATE orders SET order_status=%s WHERE parcel_order_id=%s",(new_order_status, parcel_order_id,))
        conn.commit()
        return  Orders.execute_query_get_specific_order(self,get_single_order_sql,parcel_order_id)

    @staticmethod
    def update_order_location(self, parcel_order_id, new_order_location):
        get_single_order_sql =  """
                SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.parcel_order_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE parcel_order_id=%s",(parcel_order_id, ))
        check_order_exist = cur.rowcount
        if check_order_exist == 0:
            return jsonify({"Message":"No Order Found With Order Id Of "+ str(parcel_order_id)}), 200
        cur.execute("UPDATE orders SET location=%s WHERE parcel_order_id=%s",(new_order_location, parcel_order_id,))
        conn.commit()
        return  Orders.execute_query_get_specific_order(self,get_single_order_sql,parcel_order_id)

    @staticmethod
    def  get_specific_user_orders(self, user_id):
        get_all_user_orders_sql =  """
                SELECT orders.parcel_order_id,orders.price,orders.parcel_pickup_address,orders.parcel_destination_address,
                orders.receivers_names,orders.receivers_contact,orders.created_at,
                orders.order_status,orders.created_at,users.first_name,users.last_name,users.phone_contact
                FROM orders INNER JOIN users ON users.user_id = orders.senders_user_id WHERE orders.senders_user_id=%s
                ORDER BY orders.parcel_order_id;
            """
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE senders_user_id =%s",(user_id, ))
        user_exist = cur.rowcount
        if user_exist == 0:
            return jsonify({"Message":"No Orders Found For User With A User Id Of "+ str(user_id)}), 200
        cur.execute(get_all_user_orders_sql,(user_id,))
        all_user_orders_data = cur.fetchall()
        conn.commit()
        columns = ('parcel_order_id','price','parcel_pickup_address','parcel_destination_address','receivers_names',
            'receivers_contact','created_at','order_status','senders firstname','senders lastname','senders phone contact')
        results = []
        for row in all_user_orders_data:
            results.append(dict(zip(columns, row)))
        return jsonify({'Specific_order':results}), 200 
        
        
