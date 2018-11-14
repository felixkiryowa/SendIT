from flask import Flask
# import configurations
from api.config  import app_config

def create_app(config_name):
    app = Flask(__name__) 
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    
    return app

