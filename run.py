from api import create_app
from api.views.views import GetOrderApiUrls

# creating an object of GetOrderApiUrls
app_urls =  GetOrderApiUrls()
config_name = "development"
app = create_app(config_name)
app_urls.get_api_urls(app)
if __name__ == '__main__':
    app.run()