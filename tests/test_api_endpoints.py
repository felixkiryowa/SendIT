import unittest
from flask import json
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders

from run import app


class SendAPITests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.current_user = 'admin'
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
                "password":"email@123",
                "user_type":"user"
        }

        self.admin_user = {
            "first_name":"noah", 
            "last_name":"kal", 
            "email":"noah@gmail.com",
            "contact":"0700167865", 
            "username":"noah22",
            "password":"email@123",
            "user_type":"admin"
        }

        self.login_credentials_admin = {
            "username":"noah22",
            "password":"email@123"
        }

        self.login_credentials_user = {
            "username":"kiryowa22",
            "password":"email@123"
        }
        self.client().post(
            '/api/v1/users/signup',content_type='application/json',
             data=json.dumps(
                  dict(
                     first_name=self.new_user['first_name'], last_name=self.new_user['last_name'],
                     email=self.new_user['email'], contact=self.new_user['contact'], 
                     username=self.new_user['username'], password=self.new_user['password'],
                     user_type=self.new_user['user_type'] 
                     )
                 )
             )

        self.client().post(
            '/api/v1/users/signup',content_type='application/json',
             data=json.dumps(
                 dict(
                     first_name=self.admin_user['first_name'], last_name=self.admin_user['last_name'],
                     email=self.admin_user['email'], contact=self.admin_user['contact'], 
                     username=self.admin_user['username'], password=self.admin_user['password'],
                     user_type=self.admin_user['user_type'] 
                     )
                 )
        ) 

        user_login_result = self.client().post('/api/v1/users/login',content_type='application/json',
         data=json.dumps(
             dict(
                 username=self.login_credentials_user['username'], 
                 password=self.login_credentials_user['password'])
            )
             
        )

        admin_login_result = self.client().post('/api/v1/users/login',content_type='application/json',
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
        Method to check if the data is in json form.
        """
        result = self.client().post(
            '/api/v1/parcels', content_type='application/json', headers={"token": self.user_generated_token},
             data=json.dumps(dict({"order_name": "phones",
                "order_status":self.order_data["order_status"],
                "parcel_destination_address":self.order_data["parcel_destination_address"],
                "parcel_pickup_address":self.order_data["parcel_pickup_address"],
                "parcel_weight":self.order_data["parcel_weight"],
                "receivers_contact": self.order_data["receivers_contact"],
                "receivers_names": self.order_data["receivers_names"],
                "senders_contact": self.order_data["senders_contact"],
                "senders_names": self.order_data["senders_names"]})))
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
        result = self.client().get('/api/v1/parcels', headers={"token": self.admin_generated_token})
        self.assertEqual(result.status_code, 200)
       

    # Tests for updating order status 
    def test_update_specific_order(self):
        """
        Method to update an order status.
        """
        result = self.client().put('/api/v1/parcels/1/cancel', content_type='application/json', headers={"token": self.user_generated_token},
                            data=json.dumps({"order_status":"delivered"})
                     )
        self.assertEqual(result.status_code, 200)
        #fetch updated order to verify whether the order_status has changed to Delivered
        check_updated_order = self.client().get('/api/v1/parcels/1', headers={"token": self.admin_generated_token})
        self.assertEqual(check_updated_order.status_code, 200)
        json_data = json.loads(check_updated_order.data)
        #order_status value should now be Accepted
        self.assertEqual(json_data['order']['order_status'], "delivered")

    def test_get_specific_order(self):
        result = self.client().get('/api/v1/parcels/1', headers={"token": self.admin_generated_token})
        self.assertEqual(result.status_code, 200)

    def test_get_orders_of_specific_user(self):
        result = self.client().get('/api/v1/users/1/parcels', headers={"token": self.user_generated_token})
        self.assertEqual(result.status_code, 200)

    def test_if_value_order_id_is_not_string(self):
        result = self.client().get('/api/v1/parcels/'+'one', headers={"token": self.admin_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_order_id_is_a_boolean(self):
        result = self.client().get('/api/v1/parcels/True', headers={"token": self.admin_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
        
    def test_if_value_order_id_is_not_a_complex_number(self):
        result = self.client().get('/api/v1/parcels/3.69', headers={"token": self.admin_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
    
    def test_if_order_id_is_a_complex_number(self):
        result = self.client().get('/api/v1/parcels/3+j', headers={"token": self.admin_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
    
    # tests on user_id to cancel an order
    def test_if_value_user_id_is_not_string(self):
        result = self.client().put('/api/v1/parcels/one/cancel', headers={"token": self.user_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')

    def test_if_value_user_id_is_a_boolean(self):
        result = self.client().put('/api/v1/parcels/True/cancel', headers={"token": self.user_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
        
    def test_if_value_user_id_is_not_a_complex_number(self):
        result = self.client().put('/api/v1/parcels/3.69/cancel', headers={"token": self.user_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
    
    def test_if_user_id_is_a_complex_number(self):
        result = self.client().put('/api/v1/parcels/3+j/cancel', headers={"token": self.user_generated_token})
        result_data = json.loads(result.data)
        self.assertEqual(result.status_code, 400)
        self.assertEqual(result_data['message'], 'Invalid Parcel Id')
    # tests on user_id to cancel an order


if __name__ == '__main__':
    unittest.main()