import psycopg2
from flask import Flask
# import configurations
# from api.config  import app_config
app =  Flask(__name__) 
secret_key = 'thisisasceretkey'

# creating an object of GetOrderApiUrls
# conn = psycopg2.connect(database="SendIT",user="postgres",password="atagenda1@",host="localhost",port="5432")
conn = psycopg2.connect(database="testdb")

from api.views.views import GetOrderApiUrls
GetOrderApiUrls.get_api_urls(app)

# def create_app(config_name):
#     app = Flask(__name__) 
#     app.config.from_object(app_config[config_name])
#     app.config.from_pyfile('config.py')
    
#     return app


