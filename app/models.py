from werkzeug import generate_password_hash, check_password_hash
from utils import is_sequence
from app import db
from flask.ext.permissions.models import UserMixin
from app.utils import fetch_role
from sqlalchemy.ext.hybrid import hybrid_property


class User(UserMixin):
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))

    __mapper_args__ = {
        'polymorphic_identity': 'user'
    }

    def __init__(self, email, password, roles=None):
        self.email = email.lower()
        self.password = password
        UserMixin.__init__(self, roles)

    @property
    def password(self):
        raise AttributeError('The user\'s password is not stored.')

    @password.setter
    def password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User {}>".format(user.email)


class Node(db.Model):
    name = db.Column(db.String(150))
    description = db.Column(db.Text())
    on = db.Column(db.Boolean)

    def __init__(self, name, on=False, description=None):
        self.name = name
        self.on = on
        self.description = description
