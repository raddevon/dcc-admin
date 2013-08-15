from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()


user_role_table = db.Table('user_role', db.Base.metadata,
                           db.Column(
                               'user_id', db.Integer, db.ForeignKey('user.id')),
                           db.Column(
                           'role_id', db.Integer, db.ForeignKey('role.id'))
                           )

role_ability_table = db.Table('role_ability', db.Base.metadata,
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('role.id')),
                              db.Column(
                              'ability_id', db.Integer, db.ForeignKey('ability.id'))
                              )


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(54))
    roles = db.relationship('role', secondary=user_role_table, backref='users')

    def __init__(self, email, password):
        self.email = email.lower()
        self.set_password(password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.uid)

    def __repr__(self):
        return '<User {}>'.format(self.email)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    abilities = db.relationship(
        'ability', secondary=role_ability_table, backref='roles')

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class Ability(db.Model):
    __tablename__ = 'ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)
