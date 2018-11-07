"""
This module handles view routes

"""
from api.endpoints.orders import OrdersApi

class GetOrderApiUrls:

    """
    class to define method to define all api endpoints routes
    """

    def get_api_urls(self, app):
        """function defining all the api routes """
        order_view = OrdersApi.as_view('order_api')
        app.add_url_rule(
            '/api/v1/parcels', defaults={'order_id': None},
            view_func=order_view, methods=['GET',]
        )
