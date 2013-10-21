from app import app, db
from flask.ext.restful import reqparse, Resource, abort
from flask.ext.permissions.models import Role, Ability
from flask.ext.permissions.decorators import user_is
import app.models as models

api = restful.Api(app)

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


# Will this work? I'm worried about the Model.get(id) part specifically.
def fetch_record(Model, id):
    fetched_record = Model.get(id)
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

    @user_is('admin')
    def get(self, user_id):
        user = fetch_record(models.User, user_id)
        return ({'email': user.email, 'roles': user.roles})

    def put(self, user_id):
        payload = user_parser.parse_args()
        user = User(payload['email'], payload['password'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    def post(self, user_id):
        user = fetch_record(models.User, user_id)
        payload = user_parser.parse_args()
        for attribute, value in payload.iteritems():
            user.attribute = payload[attribute]
        db.session.add(user)
        db.session.commit()
        return user, 200

    @user_is('admin')
    def delete(self, user_id):
        user = fetch_record(models.User, user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204


class UserList(Resource):

    @user_is('admin')
    def get(self):
        users = models.User.get.all()
        users_dict = {}
        for user in users:
            users_dict[user.id] = {'email': user.email, 'roles': user.roles}
        return users_dict

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/users/')
