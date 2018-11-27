import os

class Config(object):
    """
    Common configurations
    """

    TESTING = False
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'thisisasceretkey')


class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""

    DATABASE = 'test_db'
    TESTING = True
    DEBUG = True


class DevelopmentConfig(Config):
    """
    Development configurations
    """

    # DATABASE_CONNECTION = os.getenv("DATABASE_CONNECTION","postgres://YourUserName:YourPassword@YourHost:5432/YourDatabase")
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """
    Production configurations
    """

    DEBUG = False
    TESTING = True

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}