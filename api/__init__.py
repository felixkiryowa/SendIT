import psycopg2
import os 
from flask import Flask
# import configurations
# from api.config  import app_config
app =  Flask(__name__) 
secret_key = 'thisisasceretkey'

# creating an object of GetOrderApiUrls
if os.getenv('TESTING_DATABASE') == 'test_db':
    conn = psycopg2.connect(database="test_db",user="postgres",password="",host="localhost",port="5432")
conn = psycopg2.connect(database="SendIT",user="postgres",password="atagenda1@",host="localhost",port="5432")
# conn = psycopg2.connect(database="d7to87pvcitck8",user="cydhaaqyvycwlm",password="7b0226b6a6d1acdde593d5c6b628ebfc3b4a6f6439dd2e89c72ae9c96dc45ee6",host="ec2-23-23-101-25.compute-1.amazonaws.com",port="5432")

# conn = psycopg2.connect(database="SendIT")

from api.views.views import GetOrderApiUrls
GetOrderApiUrls.get_api_urls(app)

# def create_app(config_name):
#     app = Flask(__name__) 
#     app.config.from_object(app_config[config_name])
#     app.config.from_pyfile('config.py')
    
#     return app


