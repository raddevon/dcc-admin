from werkzeug import generate_password_hash, check_password_hash
from utils import is_sequence
from app import db
from flask.ext.permissions.models import UserMixin
from app.utils import fetch_role
from sqlalchemy.ext.hybrid import hybrid_property


class User(UserMixin):
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))

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

    @hybrid_property
    def assigned_roles(self):
        return [role.name for role in self.roles]

    @assigned_roles.setter
    def assigned_roles(self, roles):
        self.roles = [fetch_role(role) for role in roles]

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def __str__(self):
        return self.email

    def __repr__(self):
        return "<User {}>".format(user.email)
