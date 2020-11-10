from app import App
from app.config import ProductionConfig as app_config

app = App(app_config).app
