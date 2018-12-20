"""
This module handles view routes

"""
from api.views.users import AuthUsers
from api.views.orders import OrdersApi
from api.views.get_specific_user_orders import UserSpecificOrders
from api.views.get_specific_user_order import UserSpecificOrder
from api.views.update_order_status import UpdateUserOrderStatus
from api.views.update_order_present_location import UpdateOrderPresentLocation
from api.views.cancel_order import CancelOrder
from api.views.blacklist_tokens import BlacklistToken
from api.views.get_order_statistics import OrdersStatistics
from api.views.filter_orders import FilterOrders

class GetOrderApiUrls:
    """
    class to define method to define all api endpoints routes
    """
    @staticmethod
    def get_api_urls(app):
        """function defining all the api routes """
        order_view = OrdersApi.as_view('order_api')
        user_specific_orders_view = UserSpecificOrders.as_view('user_orders')
        specific_order_view = UserSpecificOrder.as_view('user_order')
        auth_users_view = AuthUsers.as_view('user_auth')
        update_order_status = UpdateUserOrderStatus.as_view('update_status')
        update_order_present_location = UpdateOrderPresentLocation.as_view('order_location')
        cancel_order = CancelOrder.as_view('cancel_order')
        blacklist_token = BlacklistToken.as_view('blacklist_tokens')
        order_stats = OrdersStatistics.as_view('stats')
        filter_orders = FilterOrders.as_view('filters')

        app.add_url_rule(
            '/api/v2/auth/signup', view_func=auth_users_view,
            methods=['POST',]
        )
        app.add_url_rule(
            '/api/v2/auth/login', view_func=auth_users_view,
            methods=['POST',]
        )

        app.add_url_rule(
            '/api/v2/filter/orders', view_func=filter_orders,
            methods=['POST',]
        )

        app.add_url_rule(
            '/api/v2/auth/blacklisttoken', view_func=blacklist_token,
            methods=['POST',]
        )
        app.add_url_rule(
            '/api/v2/parcels', defaults={'parcel_order_id': None},
            view_func=order_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v2/stats',
            view_func=order_stats, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v2/parcels/<parcel_order_id>',
            view_func=order_view, methods=['GET',]
        )
        app.add_url_rule('/api/v2/parcels', view_func=order_view, methods=['POST',])

        app.add_url_rule(
            '/api/v2/users/parcels',
            view_func=user_specific_orders_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v2/users/parcels/<parcel_id>',
            view_func=specific_order_view, methods=['GET',]
        )
        app.add_url_rule(
            '/api/v2/parcels/<parcel_id>/cancel', view_func=cancel_order,
            methods=['PUT',]
        )
        app.add_url_rule(
            '/api/v2/parcels/delivered', view_func=cancel_order,
            methods=['GET',]
        )
        app.add_url_rule(
            '/api/v2/parcels/<parcel_id>/status', view_func=update_order_status,
            methods=['PUT',]
        )

        app.add_url_rule(
            '/api/v2/parcels/<parcel_id>/destination',
            view_func=user_specific_orders_view, methods=['PUT',]
        )

        app.add_url_rule(
            '/api/v2/parcels/<parcel_id>/presentlocation',
            view_func=update_order_present_location, methods=['PUT',]
        )
       

