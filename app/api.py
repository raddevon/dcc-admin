from app import app, db
from flask.ext.restful import reqparse, Resource, abort
from flask.ext.permissions.models import Role, Ability
from app.models import User as UserModel

api = restful.Api(app)

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, "The user id should be an  integer.")


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
