from flask import Flask
from config import DATABASE_URI
from models import db

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
db.init_app(app)

from app import views
