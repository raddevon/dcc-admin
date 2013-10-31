from app import app, db
from flask.ext.restful import reqparse, Resource, abort, Api
from flask.ext.permissions.models import Role, Ability
import models
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.permissions.decorators import user_is
from werkzeug import generate_password_hash
import app.models as models

api = Api(app)
auth = HTTPBasicAuth()


def get_user_record(email):
    return models.User.query.filter_by(email=email).first()


def get_httpauth_user_record():
    return get_user_record(auth.username())


@auth.get_password
def get_password(username):
    user = get_user_record(username)
    return user.pwdhash


@auth.hash_password
def hash_pw(password):
    return generate_password_hash(password)


user_parser = reqparse.RequestParser()
# Would rather restrict type of this argument to a properly formatted
# email address
user_parser.add_argument(
    'email', type=str, required=True, help="Please provide an email address for the user.")
user_parser.add_argument(
    'password', type=str, required=True, help="Please provide a password for the user.")
# Will type=Role work?
user_parser.add_argument(
    'roles', type=Role, help="Optionally provide roles to be assigned to the user")


def fetch_record(Model, id):
    fetched_record = Model.query.get(id)
    if not fetched_record:
        abort(404, message="Requested record does not exist in the database.")
    return fetched_record


class Node(Resource):

    def get(self, node_id):
        pass

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


class NodeList(Resource):

    def get(self):
        pass


class User(Resource):

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self, user_id):
        user = fetch_record(models.User, user_id)
        return ({'email': user.email, 'roles': user.roles})

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self, user_id):
        user = fetch_record(models.User, user_id)
        payload = user_parser.parse_args()
        for attribute, value in payload.iteritems():
            user.attribute = payload[attribute]
        db.session.add(user)
        db.session.commit()
        return user, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def delete(self, user_id):
        user = fetch_record(models.User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserList(Resource):

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        users = models.User.query.all()
        users_dict = {}
        for user in users:
            users_dict[user.id] = {
                'email': user.email, 'roles': [{'name': role.name, 'id': role.id} for role in user.roles]}
        return users_dict, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self):
        payload = user_parser.parse_args()
        user = models.User(payload['email'], payload['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/users/')
