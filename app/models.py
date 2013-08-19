from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from utils import is_sequence

db = SQLAlchemy()


user_role_table = db.Table('user_role',
                           db.Column(
                               'user_id', db.Integer, db.ForeignKey('user.uid')),
                           db.Column(
                           'role_id', db.Integer, db.ForeignKey('role.id'))
                           )

role_ability_table = db.Table('role_ability',
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('role.id')),
                              db.Column(
                              'ability_id', db.Integer, db.ForeignKey('ability.id'))
                              )


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    abilities = db.relationship(
        'Ability', secondary=role_ability_table, backref='roles')

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __str__(self):
        return self.name


class Ability(db.Model):
    __tablename__ = 'ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)

    def __str__(self):
        return self.name


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    pwdhash = db.Column(db.String(100))
    roles = db.relationship('Role', secondary=user_role_table, backref='users')

    def __init__(self, email, password, roles=None):
        self.email = email.lower()

        # If only a string is passed for roles, convert it to a list containing
        # that string
        if roles and isinstance(roles, basestring):
            roles = [roles]

        # If a sequence is passed for roles (or if roles has been converted to
        # a sequence), fetch the corresponding database objects and make a list
        # of those.
        if roles and is_sequence(roles):
            role_list = []
            for role in roles:
                role_list.appen(Role.query.filter_by(name=role).first())
            self.roles = role_list
        # Otherwise, assign the default 'user' role. Create that role if it
        # doesn't exist.
        else:
            r = Role.query.filter_by(name='user').first()
            if not r:
                r = Role('user')
                db.session.add(r)
                db.session.commit()
            self.roles = [r]

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

    def __str__(self):
        return self.email
