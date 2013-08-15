import os

basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']
MIGRATE_REPO = os.path.join(basedir, 'migrations')
