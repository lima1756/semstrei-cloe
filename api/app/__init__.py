import os

from flask import Flask 

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'app.config.DevelopmentConfig' # TODO: For production we would want to use ProductionConfig instead of DevelopmentConfig
)
app.config.from_object(app_settings)

from app import routes