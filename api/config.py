import os


class Config(object):
    """Parent configuration class."""
    DEBUG = False

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True


app_config = {
    'development': DevelopmentConfig
}