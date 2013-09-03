try:
    from .core import db
except ImportError:
    raise Exception(
        'Permissions app must be initialized before importing models')

from werkzeug import generate_password_hash, check_password_hash
from .utils import is_sequence


user_role_table = db.Table('fp_user_role',
                           db.Column(
                               'user_id', db.Integer, db.ForeignKey('fp_user.id')),
                           db.Column(
                           'role_id', db.Integer, db.ForeignKey('fp_role.id'))
                           )

role_ability_table = db.Table('fp_role_ability',
                              db.Column(
                                  'role_id', db.Integer, db.ForeignKey('fp_role.id')),
                              db.Column(
                              'ability_id', db.Integer, db.ForeignKey('fp_ability.id'))
                              )


class RoleMixin(db.Model):

    """
    Subclass this for your roles
    """
    __tablename__ = 'fp_role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    abilities = db.relationship(
        'AbilityMixin', secondary=role_ability_table, backref='roles')

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Role {}>'.format(self.name)

    def __str__(self):
        return self.name


class AbilityMixin(db.Model):

    """
    Subclass this for your abilities
    """
    __tablename__ = 'fp_ability'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)

    def __init__(self, name):
        self.name = name.lower()

    def __repr__(self):
        return '<Ability {}>'.format(self.name)

    def __str__(self):
        return self.name


class UserMixin(db.Model):

    """
    Subclass this for your user class
    """
    __tablename__ = 'fp_user'
    id = db.Column(db.Integer, primary_key=True)
    roles = db.relationship(
        'RoleMixin', secondary=user_role_table, backref='users')

    def __init__(self, roles=None, default_role='user'):
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
                role_list.append(Role.query.filter_by(name=role).first())
            self.roles = role_list
        # Otherwise, assign the default 'user' role. Create that role if it
        # doesn't exist.
        else:
            r = RoleMixin.query.filter_by(name=default_role).first()
            if not r:
                r = RoleMixin(default_role)
                db.session.add(r)
                db.session.commit()
            self.roles = [r]

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __repr__(self):
        return '<User {}>'.format(self.id)
