from app import App
from app.config import DevelopmentConfig as app_config

app = App(app_config).app
