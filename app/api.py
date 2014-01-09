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
    'role', type=int, action='append', help="Optionally provide roles to be assigned to the user")


role_parser = reqparse.RequestParser()
role_parser.add_argument(
    'name', type=str, required=True, help="Each role needs a name.")


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

    # Getting "You do not have access" when testing this resource with cURL
    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self, user_id):
        user = fetch_record(models.User, user_id)
        payload = user_parser.parse_args()
        for attribute, value in payload.iteritems():
            if attribute == 'role':
                user.roles = [fetch_record(perms_models.Roles, role)
                              for role in payload['role']]
            else:
                user.attribute = payload[attribute]
        print user.roles
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
    def post(self):
        payload = user_parser.parse_args()
        user = models.User(payload['email'], payload['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201, {'Location': '/api/user/{}'.format(user.id)}


class Role(Resource):

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self, role_id):
        user = fetch_record(perms_models.Role, role_id)
        return ({'name': role.name, 'id': role.id})

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def post(self, role_id):
        role = fetch_record(perms_models.Role, role_id)
        payload = role_parser.parse_args()
        for attribute, value in payload.iteritems():
            role.attribute = payload[attribute]
        db.session.add(role)
        db.session.commit()
        return role, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def delete(self, role_id):
        role = fetch_record(perms_models.Role, role_id)
        db.session.delete(role)
        db.session.commit()
        return '', 204


class RoleList(Resource):

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def get(self):
        roles = perms_models.Role.query.all()
        roles_dict = {role.id: role.name for role in roles}
        return roles_dict, 200

    @auth.login_required
    @user_is('admin', get_httpauth_user_record)
    def put(self):
        payload = role_parser.parse_args()
        role = perms_models.Role(payload['name'])
        db.session.add(role)
        db.session.commit()
        return role, 201, {'Location': '/api/role/{}'.format(role.id)}

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/user/')
api.add_resource(Role, '/api/role/<string:role_id>')
api.add_resource(RoleList, '/api/role/')
