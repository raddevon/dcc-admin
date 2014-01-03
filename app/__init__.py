from flask import Flask
from flask.ext.login import LoginManager, current_user
from config import DATABASE_URI
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.permissions.core import Permissions


app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Permissions
perms = Permissions(app, db, current_user)

from app import views, auth, api
