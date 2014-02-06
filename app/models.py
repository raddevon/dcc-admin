from werkzeug import generate_password_hash, check_password_hash
from utils import is_sequence
from app import db
from flask.ext.permissions.models import UserMixin


class User(UserMixin):
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))

    def __init__(self, email, password, roles=None):
        self.email = email.lower()
        self.set_password(password)
        UserMixin.__init__(self, roles)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User {}>".format(user.email)
