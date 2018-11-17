from  run import conn
from flask import jsonify
from werkzeug.security import generate_password_hash ,check_password_hash
import jwt
import datetime
from flask import current_app

cur = conn.cursor()


class UserAuthentication(object):

    cur.execute(
          """
           CREATE TABLE IF NOT EXISTS users  (
                user_id SERIAL PRIMARY KEY,
                first_name VARCHAR(200) NOT NULL,
                last_name VARCHAR(200) NOT NULL,
                email VARCHAR(200) NOT NULL,
                phone_number VARCHAR(200) NULL,
                username VARCHAR(255) NOT NULL UNIQUE, 
                password VARCHAR(255) NOT NULL,
                user_type VARCHAR(200) NOT NULL
            )
            """
    )
    
    def __init__(self, first_name, last_name, email, phone_number,  username, password, user_type):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.username = username
        self.password = password
        self.user_type = user_type

    def execute_add_new_user_query(self):
        """ insert a new user into the users table """

        sql = """INSERT INTO users(first_name, last_name, email, phone_number, username, password, user_type)
                VALUES(%s,%s,%s,%s,%s,%s,%s) RETURNING user_id;"""
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute("SELECT * FROM users WHERE name =%s",(self.username, ))
        fetch_user = cur.rowcount

        if fetch_user == 1:
            return jsonify({'Message':'User already exists'}),409
        cur.execute(sql, (self.first_name, self.last_name, self.email, self.phone_number, self.username, 
        self.password, self.user_type, ))
        # commit the changes to the database
        conn.commit()


    def execute_user_login_auth(self, username, password,error_message):
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s",(username, ))
        specific_user = cur.fetchall()
        user_exist = cur.rowcount
        if user_exist == 0:
            return jsonify({"Message":error_message}),401
        user_password = specific_user[0][3]
        return generate_token(user_password, password, error_message)

    def generate_token(self, user_password, password, error_message):
        if check_password_hash(user_password, password):
            user_username = specific_user[0][2]
            token = jwt.encode({'username':user_username, 'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},secret_key)
            # return jsonify({'token_generated':token.decode('UTF-8')}) 
            return jsonify({'token_generated':token.decode('UTF-8')}),200
        return jsonify({"Message":error_message}),401

          
     

