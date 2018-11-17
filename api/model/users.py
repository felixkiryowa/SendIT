"""This is users class defining the users class model constructor """
from  api.db_connection import conn
from api import secret_key
from flask import jsonify
from werkzeug.security import generate_password_hash ,check_password_hash
import jwt
import datetime




class AuthUser:

    def __init__(self, *args):
        """This is AuthUsers class constructor"""
        self.first_name = args[0]
        self.last_name = args[1]
        self.email = args[2]
        self.phone_contact = args[3]
        self.username = args[4]
        self.user_password = args[5]
        self.user_type = args[6]

    @staticmethod
    def create_users_table():
        cur = conn.cursor()
        cur.execute(
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
        conn.commit()
    
    def execute_add_new_user_query(self):
        """ insert a new user into the users table """
        sql = """INSERT INTO users(first_name, last_name, email, phone_contact, username, user_password, user_type)
        VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
        # create a new cursor
        cur = conn.cursor()
        cur.execute(sql, (self.first_name, self.last_name, self.email, self.phone_contact, 
        self.username, self.user_password, self.user_type, ))
        # commit the changes to the database
        conn.commit()
        return jsonify({'Message':'You registered successfully.'}),201
    
    @staticmethod  
    def execute_user_login_auth(self, username, sent_password,error_message):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(username, ))
        specific_user = cur.fetchall()
        user_exist = cur.rowcount
        if user_exist == 0:
            return jsonify({"Message":error_message}),401
        user_username = specific_user[0][5]
        user_password = specific_user[0][6]
        
        return AuthUser.generate_token(self,user_username, user_password, sent_password, error_message, specific_user)
   
    @staticmethod
    def generate_token(self,user_username,user_password, sent_password, error_message, specific_user):
        if check_password_hash(user_password, sent_password):
            token = jwt.encode({'username':user_username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
            return jsonify({'token_generated':token.decode('UTF-8')}),200
        return jsonify({"Message":error_message}),401


