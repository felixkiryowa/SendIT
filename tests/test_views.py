from api import app ,conn
import unittest
import os
import json



class ApiTestCase(unittest.TestCase):

    """This class represents the order api test case"""

    def setUp(self):

        """Define test variables and initialize app."""
        self.client = app.test_client

        self.user_data = {
            "name":"Francis Kiryowa",
            "username":"kiryowa22",
            "password":"user123",
            "address":"Nalukolongo",
            "phone_number":"0700162509",
            "user_type":"admin"
        }

        self.customer_user = {
            "name":"Mpiima Deo",
            "username":"deo22",
            "password":"user123",
            "address":"Nakawa",
            "phone_number":"0700167896",
            "user_type":"user"
        }

        self.login_credentials_admin = {
            "username":"kiryowa22",
            "password":"user123"
        }
        self.login_credentials_user = {
            "username":"deo22",
            "password":"user123"
        }
        self.order_status =   {
                "order_status":"Processing"
            }

        self.menu = {
            "item_name":"Pizza",
            "price":50000,
            "current_items":40
          }
        self.order = {
            "item_id":1,
            "quantity":5
        }
        self.client().post(
            '/api/v2/auth/signup',content_type='application/json',
             data=json.dumps(self.user_data))
        self.client().post(
            '/api/v2/auth/signup',content_type='application/json',
             data=json.dumps(self.customer_user))

        res = self.client().post('/api/v2/auth/login',content_type='application/json',
         data=json.dumps(
             self.login_credentials_admin
             )
        )

        user = self.client().post('/api/v2/auth/login', content_type='application/json',
         data=json.dumps(self.login_credentials_user)
         )
        # self.result = json.loads(res.data.decode())
        
        # print(self.result,"token data")
        self.result = json.loads(res.data)
        self.result2 = json.loads(user.data)
        self.generated_token = self.result['token_generated']
        print(self.generated_token,'admin token')
        self.user_generated_token = self.result2['token_generated']
        print(self.user_generated_token,'user generated token')

        self.auth_header = {
        'token': self.generated_token
        }
        self.user_auth_header = {
        'token': self.user_generated_token
        }
        

    def tearDown(self):
        """
        Close connection after running database executions
        :return:
        """
        conn.commit()

    def test_add_new_menu(self):
        res = self.client().post('/api/v2/menu',content_type='application/json',
            data=json.dumps(self.menu), headers=self.auth_header)
        self.assertEqual(res.status_code,201)


        

