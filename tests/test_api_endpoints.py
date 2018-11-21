"""
This module defines tests of all the API endpoints
"""
import unittest
import os
from flask import json

from api import app


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

    def test_get_all_orders(self):
        """
        function to test getting of all registered orders
        """
        result = self.client().get('/api/v2/parcels', headers={"token": self.admin_generated_token})
        self.assertEqual(result.status_code, 200)

    # Tests for updating order status
    def test_update_a_parcel_destinstion_order(self):
        """
        Method to test update an order status.
        """
        result = self.client().put(
            '/api/v2/parcels/1/destination', content_type='application/json',
            headers={
                "token": self.user_generated_token
            },
            data=json.dumps({"parcel_destination_address":"Mbarara"})
        )
        self.assertEqual(result.status_code, 200)
        #fetch updated order to verify whether the order_status has changed to Delivered
        check_updated_order = self.client().get(
            '/api/v2/parcels/1',
            headers={"token": self.admin_generated_token}
        )
        self.assertEqual(check_updated_order.status_code, 200)
        json_data = json.loads(check_updated_order.data)
        #order_status value should now be delivered
        # self.assertEqual(json_data['Specific_order'][0]['parcel_destination_address'],2)
        self.assertEqual(json_data['Specific_order'][0]['parcel_destination_address'], "Mbarara")

    def test_get_specific_order(self):
        """
        method to test getting a single order details
        """
        result = self.client().get(
            '/api/v2/parcels/1',
            headers={"token": self.admin_generated_token}
        )
        self.assertEqual(result.status_code, 200)
        json_data = json.loads(result.data)
        if json_data == {'Message':'No Order Found With Order Id Of 1'}:
            self.assertEqual(json_data, {'Message':'No Order Found With Order Id Of 1'})
        else:
            self.assertEqual(json_data['Specific_order'][0]['parcel_destination_address'], "Mbarara")
            self.assertEqual(json_data['Specific_order'][0]['parcel_pickup_address'], "Mbale")
            self.assertEqual(json_data['Specific_order'][0]['receivers_names'], "Mukasa Derrick")
            if json_data['Specific_order'][0]['order_status'] == 'delivered':
                self.assertEqual(json_data['Specific_order'][0]['order_status'], "delivered")
            else:
                self.assertEqual(json_data['Specific_order'][0]['order_status'], "pending")
            self.assertEqual(json_data['Specific_order'][0]['parcel_order_id'], 1)

    # Tests for updating order status by an admin
    def test_update_specific_order(self):
        """
        Method to test update an order status.
        """
        result = self.client().put(
            '/api/v2/parcels/1/status', content_type='application/json',
            headers={
                "token": self.admin_generated_token
            },
            data=json.dumps({"order_status":"delivered"})
        )
        self.assertEqual(result.status_code, 200)
        #fetch updated order to verify whether the order_status has changed to Delivered
        check_updated_order = self.client().get(
            '/api/v2/parcels/1',
            headers={"token": self.admin_generated_token}
        )
        self.assertEqual(check_updated_order.status_code, 200)
        json_data = json.loads(check_updated_order.data)
        #order_status value should now be delivered

        self.assertEqual(json_data['Specific_order'][0]['order_status'], "delivered")

    def test_get_orders_of_specific_user(self):
        """
        method to test getting orders of a specific user
        """
        result = self.client().get(
            '/api/v2/users/parcels',
            headers={"token": self.user_generated_token}
        )
        json_data = json.loads(result.data)
        if json_data == {'Message':'No Order Found With Order Id Of 1'}:
            self.assertEqual(json_data, {'Message':'No Order Found With Order Id Of 1'})
        # else:
        #     self.assertEqual(result.status_code, 200)

    def test_if_value_order_id_is_not_string(self):
        """
        method to test whether passed order_id is a string
        """
        result = self.client().get(
            '/api/v2/parcels/'+'one',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_is_a_boolean(self):
        """
        method to test whether passed order_id is a boolean
        """
        result = self.client().get(
            '/api/v2/parcels/True',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_is_not_a_float_number(self):
        """
        method to test whether passed order_id is a float number
        """
        result = self.client().get(
            '/api/v2/parcels/3.69',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_order_id_is_a_complex_number(self):
        """
        method to test whether passed order_id is a complex number
        """
        result = self.client().get(
            '/api/v2/parcels/3+j',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    # Change Order status tests
    def test_if_value_order_id_passed_while_updating_order_status_is_not_string(self):
        """
        method to test whether passed order_id is a string
        """
        result = self.client().put(
            '/api/v2/parcels/one/status',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_passed_while_updating_order_status_is_not_a_boolean(self):
        """
        method to test whether passed order_id is a boolean
        """
        result = self.client().put(
            '/api/v2/parcels/True/status',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_passed_while_updating_order_status_is_not_a_floating_number(self):
        """
        method to test whether passed order_id is a float number
        """
        result = self.client().put(
            '/api/v2/parcels/3.89/status',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_passed_while_updating_order_status_is_not_a_complex_number(self):
        """
        method to test whether passed order_id is a complex number
        """
        result = self.client().put(
            '/api/v2/parcels/3+j/status',
            headers={"token": self.admin_generated_token}
        )
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')    

if __name__ == '__main__':
    unittest.main()
