from ..tasks.config import db_nsi_url, db_mm_url, db_mm_master_url
from ..config import ADMIN_USER, ADMIN_PASSW, ADMIN_NAME
import sqlalchemy as db
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


db_alchemy = SQLAlchemy()
database_nsi_engine = db.create_engine(db_nsi_url, echo=False)
database_mm_engine = db.create_engine(db_mm_url, echo=False)
database_mm_master_engine = db.create_engine(db_mm_master_url, echo=False)


class User(UserMixin, db_alchemy.Model):
    __tablename__ = 'nsi_users'

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def is_authenticated(self):
        return self.authenticated

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


def initial_setup():
    db_alchemy.create_all()
    admin = User.query.filter_by(login='admin').first()
    if not admin:
        admin_add = User(login=ADMIN_USER, name=ADMIN_NAME)
        admin_add.set_password(ADMIN_PASSW)
        db_alchemy.session.add(admin_add)
        db_alchemy.session.commit()


class Config(db_alchemy.Model):
    __tablename__ = 'nsi_tables_config'
    ID = db_alchemy.Column(db_alchemy.Integer, primary_key=True)
    NSI_TABLE_NAME = db_alchemy.Column(db_alchemy.String(256))
    OID = db_alchemy.Column(db_alchemy.String(128))
    MMDB_TABLE_NAME = db_alchemy.Column(db_alchemy.String(256))
    DICT_NAME = db_alchemy.Column(db_alchemy.String(256))
    COLUMN_MATCHING = db_alchemy.Column(db_alchemy.PickleType())
    COLUMN_UPDATE = db_alchemy.Column(db_alchemy.PickleType())
    COLUMN_CONVERT = db_alchemy.Column(db_alchemy.PickleType())
    COLUMN_EXTRA = db_alchemy.Column(db_alchemy.PickleType())
