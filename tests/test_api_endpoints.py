"""
This module defines tests of all the API endpoints
"""
import unittest
import os
from flask import json

from run import app


class SendAPITests(unittest.TestCase):
    """
    SendAPITests unittests class
    """
    def setUp(self):
        """
        function to define all test setup variables
        """
        self.test_database = os.getenv('TEST_DATABASE','test_db')
        self.app = app
        self.current_user = 'admin'
        self.client = app.test_client
        self.order_data = {
            "order_name":"Phones",
            "parcel_weight":4, 
            "parcel_pickup_address":"Mbale", 
            "parcel_destination_address":"Gulu", 
            "receivers_names":"Mukasa Derrick", 
            "receivers_contact":"0789564312"
        }

        self.new_user = {
                "first_name":"Francis",
                "last_name":"Kiryowa",
                "email":"fk@gmail.com",
                "phone_contact":"0700162509",
                "username": "kiryowa22",
                "user_password": "user123",
                "user_type":"user"   
        }
     

        self.admin_user = {
            "first_name":"Mark",
            "last_name":"Kajubi",
            "email":"mark@email.com",
            "phone_contact":"0789906754",
            "username": "mark22",
            "user_password": "user123",
            "user_type":"admin"
        }

        self.login_credentials_admin = {
            "username":"mark22",
            "password":"user123"
        }

        self.login_credentials_user = {
            "username":"kiryowa22",
            "password":"user123"
        }  
        self.client().post(
            '/api/v2/auth/signup', content_type='application/json',
            data=json.dumps(
                dict(
                    first_name=self.new_user['first_name'], last_name=self.new_user['last_name'],
                    email=self.new_user['email'], phone_contact=self.new_user['phone_contact'],
                    username=self.new_user['username'], user_password=self.new_user['user_password'],
                    user_type=self.new_user['user_type']
                )
            )
        )

        self.client().post(
            '/api/v2/auth/signup', content_type='application/json',
            data=json.dumps(
                dict(
                    first_name=self.admin_user['first_name'], last_name=self.admin_user['last_name'],
                    email=self.admin_user['email'], phone_contact=self.admin_user['phone_contact'],
                    username=self.admin_user['username'], user_password=self.admin_user['user_password'],
                    user_type=self.admin_user['user_type']
                )
            )
        )

        user_login_result = self.client().post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps(
                dict(
                    username=self.login_credentials_user['username'],
                    password=self.login_credentials_user['password']
                )
            )
        )

        admin_login_result = self.client().post(
            '/api/v2/auth/login', content_type='application/json',
            data=json.dumps(
                dict(
                    username=self.login_credentials_admin['username'],
                    password=self.login_credentials_admin['password']
                )
            )
        )
        self.result = json.loads(user_login_result.data)
        self.user_generated_token = self.result['token_generated']
        self.result2 = json.loads(admin_login_result.data)
        self.admin_generated_token = self.result2['token_generated']

        
    # Tests for addng a new order
    def test_if_data_posted_is_in_form_of_json(self):
        """
        Method to check if the posted parcel order data is in json form.
        """
        result = self.client().post(
            '/api/v2/parcels', content_type='application/json',
            headers={"token": self.user_generated_token},
            data=json.dumps(
                dict(
                    {
                        "order_name":self.order_data["order_name"],
                        "parcel_weight":self.order_data["parcel_weight"],
                        "parcel_pickup_address":self.order_data["parcel_pickup_address"],
                        "parcel_destination_address":self.order_data["parcel_destination_address"],
                        "receivers_names": self.order_data["receivers_names"],
                        "receivers_contact": self.order_data["receivers_contact"],
                    }
                )
            )
        )
        self.assertEqual(result.status_code, 201)
        # Json data
        order_data = json.loads(result.data)
        #testing  whether order was saved with the same attributes and values
        self.assertEqual(self.order_data["order_name"], "Phones")
        self.assertEqual(self.order_data["parcel_weight"], 4)
        self.assertEqual(self.order_data["parcel_pickup_address"], "Mbale")
        self.assertEqual(self.order_data["parcel_destination_address"], "Gulu")
        self.assertEqual(self.order_data["receivers_names"], "Mukasa Derrick")
        self.assertEqual(self.order_data["receivers_contact"], "0789564312")  
    #tests on user user_id to get orders of a specific user

if __name__ == '__main__':
    unittest.main()
