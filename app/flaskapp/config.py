from flaskapp.tasks.config import db_nsi_url

APP_PORT = 5000
APP_HOST = '0.0.0.0'
TESTING = True
DEBUG = True
ENV = 'development'
SECRET_KEY = 'b710e23fa9ba8d05bccb8d4dc94a8fdb49b5cf25976b484cdd412b621f2f87a4'
ADMIN_USER = 'admin'
ADMIN_PASSW = 'admin'
ADMIN_NAME = 'Администратор'

LOG_FORMAT = '%(asctime)s [%(levelname)s] %(name)s : (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
MAX_BYTES = 10000000
BACKUP_COUNT = 9

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = db_nsi_url
