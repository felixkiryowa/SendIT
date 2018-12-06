"""This is users class defining the users class model constructor """
from  api import connection
from api import secret_key
from flask import jsonify
from werkzeug.security import generate_password_hash ,check_password_hash
import jwt
import datetime



cursor = connection.cursor()

class AuthUser:

    cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users  (
                user_id SERIAL PRIMARY KEY,
                first_name VARCHAR(200) NOT NULL,
                last_name VARCHAR(200) NOT NULL,
                email VARCHAR(200) NOT NULL,
                phone_contact VARCHAR(200) NULL,
                username VARCHAR(255) NOT NULL UNIQUE, 
                user_password VARCHAR(255) NOT NULL,
                user_type VARCHAR(200) NOT NULL
            )
            """
    )

    def __init__(self, *args):
        """This is AuthUsers class constructor"""
        self.first_name = args[0]
        self.last_name = args[1]
        self.email = args[2]
        self.phone_contact = args[3]
        self.username = args[4]
        self.user_password = args[5]
        self.user_type = args[6]

    
    def execute_add_new_user_query(self):
        """ insert a new user into the users table """
        sql = """INSERT INTO users(first_name, last_name, email, phone_contact, username, user_password, user_type)
        VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
        # create a new cursorsor
        cursor = connection.cursor()
        cursor.execute(sql, (self.first_name, self.last_name, self.email, self.phone_contact, 
        self.username, self.user_password, self.user_type, ))
        # commit the changes to the database
        connection.commit()
    
    @staticmethod  
    def execute_user_login_auth(self, username, login_password,error_message):
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s",(username, ))
        user_data = cursor.fetchall()
        user = cursor.rowcount
        if user == 0:
            handle_error = {
                'message':error_message
            }
            return jsonify({'login_message': handle_error}),401
            # return jsonify({"message":error_message}),401
        user_id = user_data[0][0]
        user_password = user_data[0][6]
        user_role = user_data[0][7]
        username = user_data[0][5]
        
        return AuthUser.generate_token(self,user_id, user_password, user_role, username, login_password, error_message, user_data)
   
    @staticmethod
    def generate_token(self, user_id, user_password, user_role, username, login_password, error_message, user_data):
        if check_password_hash(user_password, login_password):
            token = jwt.encode(
                {'user_id':user_id, 
                'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, 
                secret_key, algorithm='HS256')
            login_response = {
                'username':username,
                'user_role':user_role,
                'message':'successfully loggedin',
                'token_generated':token.decode('UTF-8')
            }
            
            return jsonify({'login_message':login_response}),200
        handle_error = {
            'message':error_message
        }
        return jsonify({"login_message": handle_error}),401

    @staticmethod
    def create_default_admin_user():
        """
        method to create default admin user
        """
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users  (
                user_id SERIAL PRIMARY KEY,
                first_name VARCHAR(200) NOT NULL,
                last_name VARCHAR(200) NOT NULL,
                email VARCHAR(200) NOT NULL,
                phone_contact VARCHAR(200) NULL,
                username VARCHAR(255) NOT NULL UNIQUE, 
                user_password VARCHAR(255) NOT NULL,
                user_type VARCHAR(200) NOT NULL
            )
            """
        )
        admin_password = generate_password_hash("user123")
        cursor.execute("SELECT * FROM users WHERE username =%s AND email=%s",("mark22", "mark@email.com", ))
        user = cursor.rowcount
        if user >= 1:
            return True
        sql = """INSERT INTO users(first_name, last_name, email, phone_contact, username, 
        user_password, user_type)
        VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
        # create a new cursorsor
        cursor = connection.cursor()
        cursor.execute(sql, ("mark", "kajubi", "mark@email.com", "0789906754", 
        "mark22", admin_password, "admin", ))
        # commit the changes to the database
        connection.commit()


