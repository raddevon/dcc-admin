from flask import Flask
from flask.ext.login import LoginManager
from config import DATABASE_URI
from models import db

app = Flask(__name__)
app.config.from_object('config')

# Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

from app import views, auth
