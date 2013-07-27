import os

CSRF_ENABLED = True
SECRET_KEY = os.environ['SECRET_KEY']
DATABASE_URI = os.environ['DATABASE_URI']