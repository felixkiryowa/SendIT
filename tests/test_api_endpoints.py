import unittest
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders
from run import app


class SendAPITests(unittest.TestCase):
    
    def setUp(self):
        self.app = app
        self.client = app.test_client
        self.order = OrdersApi()

    def test_get_all_orders(self):
        result = self.client().get('/api/v1/parcels')
        self.assertEqual(result.status_code, 200)