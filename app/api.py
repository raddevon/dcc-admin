from app import app, db
from flask.ext.restful import reqparse, Resource, abort, Api
from flask.ext.permissions import models as perms_models
import models
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.permissions.decorators import user_is
from werkzeug import generate_password_hash, check_password_hash
import app.models as models
from app.utils import fetch_record, fetch_role
from functools import wraps
import json
from flask import request

api = Api(app)


def accept_json(func):
    """
    Decorator which returns a 406 Not Acceptable if the client won't accept JSON
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        accept = api.mediatypes()
        if "*/*" in accept or "application/json" in accept:
            return func(*args, **kwargs)
        return {"message": "Request must accept JSON"}, 406
    return wrapper


def require_json(func):
    """
    Decorator which returns a 415 Unsupported Media Type if the client sends
    something other than JSON
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if request.mimetype == "application/json":
            return func(*args, **kwargs)
        return {"message": "Request must contain JSON"}, 415
    return wrapper


class HTTPWerkzeugBasicAuth(HTTPBasicAuth):

    def authenticate(self, auth, password):
        client_password = auth.password
        return check_password_hash(password, client_password)

auth = HTTPWerkzeugBasicAuth()


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
user_parser.add_argument(
    'email', type=str, required=True, help="Please provide an email address for the user.", location="get_json")
user_parser.add_argument(
    'password', type=str, required=True, help="Please provide a password for the user.", location="get_json")
user_parser.add_argument(
    'roles', type=list, help="Optionally provide the names of roles to be assigned to the user.", location="get_json")


role_parser = reqparse.RequestParser()
role_parser.add_argument(
    'name', type=str, required=True, help="Each role needs a name.", location="get_json")


class Node(Resource):

    method_decorators = [accept_json]

    def get(self, node_id):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class NodeList(Resource):

    method_decorators = [accept_json]

    def get(self):
        pass

    def post(self):
        pass


class User(Resource):

    method_decorators = [accept_json]

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self, user_id):
        user = fetch_record(models.User, user_id)
        return {'email': user.email, 'roles': list(user.roles)}

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    @require_json
    def put(self, user_id):
        user = fetch_record(models.User, user_id)
        payload = user_parser.parse_args()
        for attribute, value in payload.iteritems():
            setattr(user, attribute, payload[attribute])
        db.session.commit()
        user_dict = {'email': user.email}
        return user_dict, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def delete(self, user_id):
        user = fetch_record(models.User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserList(Resource):

    method_decorators = [accept_json]

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        users = models.User.query.all()
        users_dict = {}
        for user in users:
            users_dict[user.id] = {
                'email': user.email, 'roles': list(user.roles)}
        return users_dict, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self):
        payload = user_parser.parse_args()
        user = models.User(
            payload['email'], payload['password'], payload['roles'])
        db.session.add(user)
        db.session.commit()
        user_dict = {'email': user.email}
        return user_dict, 201, {'Location': '/api/user/{}'.format(user.id)}


class Role(Resource):

    method_decorators = [accept_json]

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self, role_name):
        role = fetch_role(role_name)
        return ({'name': role.name}), 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self, role_name):
        role = fetch_role(role_name)
        payload = role_parser.parse_args()
        for attribute, value in payload.iteritems():
            role.attribute = payload[attribute]
        db.session.add(role)
        db.session.commit()
        return {'name': role.name}, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def delete(self, role_name):
        role = fetch_role(role_name)
        db.session.delete(role)
        db.session.commit()
        return '', 204


class RoleList(Resource):

    method_decorators = [accept_json]

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        roles = perms_models.Role.query.all()
        return [role.name for role in roles], 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self):
        payload = role_parser.parse_args()
        role = perms_models.Role(payload['name'])
        db.session.add(role)
        db.session.commit()
        return role.name, 201, {'Location': '/api/role/{}'.format(role.name)}

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/user/')
api.add_resource(Role, '/api/role/<string:role_name>')
api.add_resource(RoleList, '/api/role/')
