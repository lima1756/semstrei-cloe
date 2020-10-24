from app import app, config, start
from app.config import ProductionConfig as app_config

config(app_config)
start()