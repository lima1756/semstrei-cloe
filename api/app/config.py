import os
import logging
from dotenv import load_dotenv
from app.libs import oracle_cx
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()


class BaseConfig:
    """Base configuration."""
    ENVIRONMENT_TYPE = "BASE"
    JWT_KEY = os.getenv('SECRET_KEY', 'a_really_secret_key')
    DEBUG = False
    LOGGING_LEVEL = logging.WARN
    LOGGING_FORMAT = '%(asctime)s %(levelname)s %(threadName)s : %(message)s'
    LOGGING_DIR = './logs/'
    LOGGING_FILE = None
    oracle_connection = oracle_cx(
        username=os.getenv('DATABASE_ORACLE_USER', 'admin'),
        password=os.getenv('DATABASE_ORACLE_PASSWORD', 'password'),
        protocol='tcps',
        host='adb.us-ashburn-1.oraclecloud.com',
        port='1522',
        service_name=os.getenv('DATABASE_ORACLE_SERVICE',
                               'key_adb_high.adb.oraclecloud.com'),
    )
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL'+ENVIRONMENT_TYPE,
        oracle_connection.get_connection_string()
    )
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_DEBUG = 0


class DevelopmentConfig(BaseConfig):
    """Development configuration."""
    ENVIRONMENT_TYPE = "DEV"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGGING_LEVEL = logging.DEBUG


class TestingConfig(BaseConfig):
    """Testing configuration."""
    ENVIRONMENT_TYPE = "TEST"
    DEBUG = True
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    LOGGING_LEVEL = logging.WARNING
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_TEST', 'sqlite:///' + os.path.join(basedir, '../tests/app/app_test.db'))


class ProductionConfig(BaseConfig):
    """Production configuration."""
    ENVIRONMENT_TYPE = "PROD"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOGGING_LEVEL = logging.DEBUG
    LOGGING_FILE = 'server.prod.log'
