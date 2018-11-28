import psycopg2
import os
from flask import Flask
from flasgger import Swagger
from flask_cors import CORS
app =  Flask(__name__)
CORS(app) 
secret_key = 'thisisasceretkey'

Swagger(app)

# connecltions to heroku database and travis
connection = psycopg2.connect(database="SendIT",user="postgres",password="atagenda1@",host="localhost",port="5432")
# if os.getenv('HEROKU_ENVIRONMENT') == 'heroku':
#     connection = psycopg2.connect(database="d7to87pvcitck8",user="cydhaaqyvycwlm",password="7b0226b6a6d1acdde593d5c6b628ebfc3b4a6f6439dd2e89c72ae9c96dc45ee6",host="ec2-23-23-101-25.compute-1.amazonaws.com",port="5432")
# else:
#     connection = psycopg2.connect(database="testdb")



from api.routes.views import GetOrderApiUrls
GetOrderApiUrls.get_api_urls(app)



