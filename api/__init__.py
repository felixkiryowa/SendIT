from flask import Flask
# import configurations
from api.config  import app_config

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    return app



# from api.views.auth_view import UserAutherizationUrls
# from api.views.menu_views import MenuUrls
# from api.views.order_view import OrderUrls
# from api.views.order_history_view import OrderHistoryUrls


# OrderUrls.order_management_urls(app)
# MenuUrls.fetch_menu_urls(app)
# OrderHistoryUrls.order_history_urls(app)
# UserAutherizationUrls.fetch_authorization_urls(app)
