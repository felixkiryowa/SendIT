"""
This module handles view routes

"""
from api.endpoints.orders import OrdersApi
from api.endpoints.get_specific_user_orders import UserSpecificOrders
from api.endpoints.users import AuthUsers

class GetOrderApiUrls:

    """
    class to define method to define all api endpoints routes
    """

    def get_api_urls(self, app):
        """function defining all the api routes """
        order_view = OrdersApi.as_view('order_api')
        user_specific_orders_view = UserSpecificOrders.as_view('user_orders')
        auth_users_view = AuthUsers.as_view('user_auth')
        app.add_url_rule(
            '/api/v1/parcels', defaults={'parcel_order_id': None},
            view_func=order_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v1/parcels/<parcel_order_id>',
             view_func=order_view, methods=['GET',]
        )
        app.add_url_rule('/api/v1/parcels', view_func=order_view, methods=['POST',])
        
        app.add_url_rule(
            '/api/v1/users/<int:user_id>/parcels',
             view_func=user_specific_orders_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v1/parcels/<order_parcel_id>/cancel', view_func=order_view, 
            methods=['PUT',]
        )
        app.add_url_rule(
            '/api/v1/users/signup', view_func=auth_users_view, 
            methods=['POST',]
        )
        app.add_url_rule(
            '/api/v1/users/login', view_func=auth_users_view, 
            methods=['POST',]
        )
