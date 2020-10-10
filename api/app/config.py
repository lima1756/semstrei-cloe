import os
import logging
basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_really_secret_key')
    DEBUG = False
    LOGGING_LEVEL = logging.WARN
    LOGGING_FORMAT = '%(asctime)s %(levelname)s %(threadName)s : %(message)s'
    LOGGING_FILE = None


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_DEV', 'sqlite:///' + os.path.join(basedir, 'app.db'))
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """Testing configuration."""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGGING_LEVEL = logging.ERROR
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_TEST', 'sqlite:///' + os.path.join(basedir, 'app_test.db'))


class ProductionConfig(BaseConfig):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', DevelopmentConfig.SQLALCHEMY_DATABASE_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
