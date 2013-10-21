from app import app, db
from flask.ext.restful import reqparse, Resource, abort
from flask.ext.permissions.models import Role, Ability
from app.models import User as UserModel

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

    def get(self, user_id):
        args = parser.parse_args()
        user = UserModel.get(args['user_id'])
        try:
            return ({'email': user.email, 'roles': user.roles})
        except AttributeError():
            return abort(404, message="User {} not found.".format(user_id))

    def put(self, user_id):
        pass

    def post(self, user_id):
        pass

    def delete(self, user_id):
        pass


class UserList(Resource):

    def get(self):
        users = UserModel.get.all()
        users_dict = {}
        for user in users:
            users_dict[user.id] = {'email': user.email, 'roles': user.roles}
        return users_dict

api.add_resource(User, '/api/user/<string:user_id>')
api.add_resource(UserList, '/api/users/')
