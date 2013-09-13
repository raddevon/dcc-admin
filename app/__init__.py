from flask import Flask
from flask.ext.login import LoginManager, current_user
from config import DATABASE_URI
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.permissions.core import Permissions

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object('config')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Flask-Permissions
perms = Permissions(app, db, current_user)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)
with app.test_request_context():
    db.create_all()

from app import views, auth
