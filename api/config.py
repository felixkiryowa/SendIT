import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'thisisasceretkey')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


app_config = {
    'development': DevelopmentConfig
}