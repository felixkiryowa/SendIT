import unittest
from flask import json
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders

from run import app


class SendAPITests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = app.test_client
        self.order = OrdersApi()
        self.user_orders = UserSpecificOrders()
        self.order_data = {
                "order_name": "phones",
                "order_status":"pending",
                "parcel_destination_address": "Mpigi",
                "parcel_pickup_address": "Kamwokya",
                "parcel_weight": 6,
                "receivers_contact": "070786543",
                "receivers_names": "mariat candance",
                "senders_contact": "0700978789",
                "senders_names": "Namyalo Agnes",
            }

        self.new_user = {
                "first_name":"francis", 
                "last_name":"kiryowa", 
                "email":"francis@gmail.com",
                "contact":"0700162509", 
                "username":"kiryowa22",
                "password":"email@123"
        }

        self.login_credentials_user = {
            "username":"kiryowa22",
            "password":"email@123"
        }
        self.client().post(
            '/api/v1/users/signup',content_type='application/json',
             data=json.dumps(self.new_user))

        user_login_result = self.client().post('/api/v1/users/login',content_type='application/json',
         data=json.dumps(dict(username=self.login_credentials_user['username'], password=self.login_credentials_user['password']))
             
        )
        
        self.result = json.loads(user_login_result.data)
        self.user_generated_token = self.result['token_generated']
        self.user_auth_header = {
        'token': self.user_generated_token
        }
        
    # Tests for addng a new order 
    def test_if_data_posted_is_in_form_of_json(self):
        """
        Method to check if the data is in json form.
        """
        result = self.client().post(
            '/api/v1/parcels', content_type='application/json',
             data=json.dumps(self.order_data), headers=self.user_auth_header)
        self.assertEqual(result.status_code, 201)
        # Json data
        order_data = json.loads(result.data)
        #testing  whether order was saved with the same attributes and values
        self.assertEqual(order_data["order_name"], "phones") 
        self.assertEqual(order_data["order_status"], "pending")
        self.assertEqual(order_data["parcel_destination_address"], "Mpigi") 
        self.assertEqual(order_data["parcel_pickup_address"], "Kamwokya") 
        self.assertEqual(order_data["parcel_weight"], 6) 
        self.assertEqual(order_data["receivers_contact"], "070786543") 
        self.assertEqual(order_data["receivers_names"], "mariat candance")
        self.assertEqual(order_data["senders_contact"], "0700978789")
        self.assertEqual(order_data["senders_names"], "Namyalo Agnes")
    
    # Test get all orders
    def test_get_all_orders(self):
        result = self.client().get('/api/v1/parcels')
        self.assertEqual(result.status_code, 200)
       

    # Tests for updating order status 
    def test_update_specific_order(self):
        """
        Method to update an order status.
        """
        result = self.client().put('/api/v1/parcels/1/cancel', content_type='application/json',
                            data=json.dumps(
                                {"order_status":"delivered"}
                                ),headers=self.user_auth_header
                                )
        self.assertEqual(result.status_code, 200)
        #fetch updated order to verify whether the order_status has changed to Delivered
        check_updated_order = self.client().get('/api/v1/parcels/1')
        self.assertEqual(check_updated_order.status_code, 200)
        json_data = json.loads(check_updated_order.data)
        #order_status value should now be Accepted
        self.assertEqual(json_data['order']['order_status'], "delivered")

    def test_get_specific_order(self):
        result = self.client().get('/api/v1/parcels/1')
        self.assertEqual(result.status_code, 200)

    def test_if_value_order_id_is_not_string(self):
        with self.assertRaises(ValueError):self.order.get("one")

    def test_if_value_order_id_is_not_an_empty_string(self):
        with self.assertRaises(ValueError):self.order.get("")

    def test_if_value_order_id_is_not_a_complex_number(self):
        with self.assertRaises(ValueError):self.order.get(2j+1)
            
    def test_if_value_order_id_is_not_a_float_point_number(self):
        with self.assertRaises(ValueError):self.order.get(3.90)

    def test_if_args_passed_to_select_specific_order_are_not_numbers(self):
        with self.assertRaises(ValueError):self.order.select_specific_order(2,2)
    
    def test_select_specific_order(self):
        self.assertTrue(self.order.select_specific_order("order_id", 1))

    def test_get_orders_of_specific_user(self):
        result = self.client().get('/api/v1/users/1/parcels')
        self.assertEqual(result.status_code, 200)

    def test_arg_passed_get_single_user_orders_is_not_a_string(self):
        with self.assertRaises(ValueError):self.user_orders.get("two")

    def test_arg_passed_get_single_user_orders_is_an_empty_string(self):
        with self.assertRaises(ValueError):self.user_orders.get("")

    def test_arg_passed_get_single_user_orders_is_a_complex_number(self):
        with self.assertRaises(ValueError):self.user_orders.get(2j)


if __name__ == '__main__':
    unittest.main()