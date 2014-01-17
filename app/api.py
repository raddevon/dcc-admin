from app import app, db
from flask.ext.restful import reqparse, Resource, abort, Api
from flask.ext.permissions import models as perms_models
import models
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.permissions.decorators import user_is
from werkzeug import generate_password_hash, check_password_hash
import app.models as models

api = Api(app)


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
    'email', type=str, required=True, help="Please provide an email address for the user.")
user_parser.add_argument(
    'password', type=str, required=True, help="Please provide a password for the user.")
user_parser.add_argument(
    'role', type=str, action='append', help="Optionally provide the names of roles to be assigned to the user.")


role_parser = reqparse.RequestParser()
role_parser.add_argument(
    'name', type=str, required=True, help="Each role needs a name.")


def fetch_record(Model, id):
    fetched_record = Model.query.get(id)
    if not fetched_record:
        abort(404, message="Requested record does not exist in the database.")
    return fetched_record


def fetch_role(name):
    fetched_role = perms_models.Role.query.filter_by(name=name).first()
    if not fetched_role:
        abort(404, message="Requested role does not exist in the database.")
    return fetched_role


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
        user.roles = [role.name for role in user.roles]
        return ({'email': user.email, 'roles': user.roles})

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self, user_id):
        user = fetch_record(models.User, user_id)
        payload = user_parser.parse_args()
        for attribute, value in payload.iteritems():
            if attribute == 'role' and value:
                user.roles = [fetch_role(role)
                              for role in payload['role']]
            else:
                user.attribute = payload[attribute]
        db.session.add(user)
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

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        users = models.User.query.all()
        users_dict = {}
        for user in users:
            users_dict[user.id] = {
                'email': user.email, 'roles': [role.name for role in user.roles]}
        return users_dict, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self):
        payload = user_parser.parse_args()
        user = models.User(
            payload['email'], payload['password'])
        for attribute, value in payload.iteritems():
            if attribute == 'role' and value:
                user.roles = [fetch_role(role)
                              for role in payload['role']]
        db.session.add(user)
        db.session.commit()
        user_dict = {'email': user.email}
        return user_dict, 201, {'Location': '/api/user/{}'.format(user.id)}


class Role(Resource):

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self, role_name):
        role = fetch_record(perms_models.Role, role_name)
        return ({'name': role.name}), 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self, role_name):
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

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        roles = perms_models.Role.query.all()
        return [role.name for role in roles], 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self):
        payload = role_parser.parse_args()
        role = perms_models.Role(payload['name'])
        db.session.add(role)
        db.session.commit()
        return role.name, 201, {'Location': '/api/role/{}'.format(role.name)}

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/user/')
api.add_resource(Role, '/api/role/<string:role_name>')
api.add_resource(RoleList, '/api/role/')
