import os
basedir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_really_secret_key')
    DEBUG = False

class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    # TODO: set development DB configuration

class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    # TODO: set testing DB configuration

class ProductionConfig(BaseConfig):
    """Production configuration."""
    # TODO: set production DB configuration