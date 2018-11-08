"""
This module handles view routes

"""
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders

class GetOrderApiUrls:

    """
    class to define method to define all api endpoints routes
    """

    def get_api_urls(self, app):
        """function defining all the api routes """
        order_view = OrdersApi.as_view('order_api')
        user_specific_orders_view = UserSpecificOrders.as_view('user_orders')
        app.add_url_rule(
            '/api/v1/parcels', defaults={'order_id': None},
            view_func=order_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v1/parcels/<int:order_id>',
             view_func=order_view, methods=['GET',]
        )
        app.add_url_rule('/api/v1/parcels', view_func=order_view, methods=['POST',])
        app.add_url_rule(
            '/api/v1/users/<int:user_id>/parcels',
             view_func=user_specific_orders_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v1/parcels/<int:parcel_id>/cancel', view_func=order_view, 
            methods=['PUT',]
        )
