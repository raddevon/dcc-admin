import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']
MIGRATE_REPO = os.path.join(basedir, 'migrations')

import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URI']


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ['DEV_DATABASE_URI']


class TestingConfig(Config):
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URI']
    # SQLALCHEMY_ECHO = True
