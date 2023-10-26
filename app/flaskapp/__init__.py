from .config import MAX_BYTES, BACKUP_COUNT, LOG_FORMAT
from .views.views import *
from .views.api import api
from .models.models import db_alchemy, initial_setup
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta
from flask import Flask
from gevent import monkey

monkey.patch_all()


def local_tz_time(*args):
    tzinfo = timezone(timedelta(hours=3.0))
    now = datetime.now(tzinfo)
    return now.timetuple()


tzinfo = timezone(timedelta(hours=3.0))
LOG_FILE = f'flaskapp/logs/app.log' #-{datetime.now(tzinfo).strftime("%d-%m-%Y-%H-%M-%S")}

log_format = logging.Formatter(LOG_FORMAT)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(log_format)
stream_handler.setLevel(logging.WARNING)
file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.WARNING)
logging.Formatter.converter = local_tz_time


def create_app():
    app = None
    try:
        app = Flask(__name__, instance_relative_config=False)
        app.logger.setLevel(logging.WARNING)
        app.logger.addHandler(stream_handler)
        app.logger.addHandler(file_handler)
        app.config.from_pyfile('config.py')
        db_alchemy.init_app(app)
        with app.app_context():
            initial_setup()
        login_manager.init_app(app)
        app.register_blueprint(view_page)
        app.register_blueprint(auth)
        api.init_app(app, add_specs=False)
    except Exception as err:
        app.logger.critical(str(err))
    else:
        return app





