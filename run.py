from api import create_app
# from flask import Flask
from api.views.views import GetOrderApiUrls
# creating an object of GetOrderApiUrls
app_config = 'development'
app =  create_app(app_config)
GetOrderApiUrls.get_api_urls(app)
if __name__ == '__main__':
    app.run(use_reloader=False)