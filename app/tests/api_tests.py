import unittest
import json
from base64 import b64encode

import app.models as models
import flask.ext.permissions.models as perms_models

import app


class ApiTests(unittest.TestCase):

    def setUp(self):
        app.app.config.from_object('config.TestingConfig')
        self.app = app.app.test_client()
        app.db.create_all()
        admin_role = perms_models.Role('admin')
        app.db.session.add(admin_role)
        app.db.session.commit()
        self.admin_email = 'raddevon@gmail.com'
        self.admin_password = '1234567'
        new_user = models.User(self.admin_email, self.admin_password, 'admin')
        app.db.session.add(new_user)
        app.db.session.commit()

        self.auth_headers = {
            'Authorization': 'Basic ' + b64encode('{0}:{1}'.format(self.admin_email, self.admin_password))
        }

    def tearDown(self):
        app.db.session.close()
        app.db.drop_all()


class UserListApiTests(ApiTests):

    def testInitialUser(self):
        response = self.app.get('/api/user/', headers=self.auth_headers)
        self.assertEqual(response.headers['Content-Type'], 'application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data.itervalues().next()['email'], self.admin_email)
        self.assertEqual(len(data), 1)

    def testAddUser(self):
        response = self.app.post(
            '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567'}, headers=self.auth_headers)
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(response.status_code, 201)

    def testAddUserWithRole(self):
        response = self.app.post(
            '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567', 'assigned_roles': 'admin'}, headers=self.auth_headers)
        user = models.User.query.filter_by(email='test@gmail.com').first()
        role = perms_models.Role.query.filter_by(name='admin').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertIn(role, user.roles)
        self.assertEqual(response.status_code, 201)

    def testAddUserWithMultipleRoles(self):
        user_role = perms_models.Role('user')
        app.db.session.add(user_role)
        app.db.session.commit()
        roles = ['admin', 'user']
        response = self.app.post(
            '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567', 'assigned_roles': roles}, headers=self.auth_headers)
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertItemsEqual(roles, user.assigned_roles)
        self.assertEqual(response.status_code, 201)


class UserApiTests(ApiTests):

    def testGetUser(self):
        response = self.app.get('/api/user/1', headers=self.auth_headers)
        user = json.loads(response.data)
        self.assertEqual(user['email'], self.admin_email)

    def testChangeExistingUser(self):
        user_role = perms_models.Role('user')
        app.db.session.add(user_role)
        app.db.session.commit()
        new_user = models.User('start@mail.com', '1234567', 'user')
        app.db.session.add(new_user)
        app.db.session.commit()
        user_changes = {'email': 'end@mail.com',
                        'password': '7654321', 'assigned_roles': ['user', 'admin']}
        response = self.app.put(
            '/api/user/' + str(new_user.id), data=user_changes, headers=self.auth_headers)
        user = models.User.query.get(new_user.id)
        self.assertEqual(user.email, user_changes['email'])
        self.assertTrue(user.check_password(user_changes['password']))
        self.assertItemsEqual(
            user.assigned_roles, user_changes['assigned_roles'])


# class RoleApiTests(ApiTests):
#     def testInitialUser(self):
#         response = self.app.get("/api/user/", headers=self.headers)
#         print response.data
#         self.assertEqual(response.headers["Content-Type"], "application/json")
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(
#             data.itervalues().next()['email'], 'raddevon@gmail.com')
#         self.assertEqual(len(data), 1)
#     def testAddUser(self):
#         response = self.app.post(
#             '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567'}, headers=self.headers)
#         user = models.User.query.filter_by(email='test@gmail.com').first()
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, 'test@gmail.com')
#         self.assertEqual(response.status_code, 201)
#     def testAddUserWithRole(self):
#         response = self.app.post(
#             '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567', 'role': 'admin'}, headers=self.headers)
#         user = models.User.query.filter_by(email='test@gmail.com').first()
#         role = perms_models.Role.query.filter_by(name='admin').first()
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, 'test@gmail.com')
#         self.assertIn(role, user.roles)
#         self.assertEqual(response.status_code, 201)
#     def testAddUserWithMultipleRoles(self):
#         user_role = perms_models.Role('user')
#         app.db.session.add(user_role)
#         app.db.session.commit()
#         response = self.app.post(
#             '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567', 'role': ['admin', 'user']}, headers=self.headers)
#         user = models.User.query.filter_by(email='test@gmail.com').first()
#         roles = [perms_models.Role.query.filter_by(
#             name='admin').first(), perms_models.Role.query.filter_by(name='user').first()]
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, 'test@gmail.com')
#         self.assertEqual(roles, user.roles)
#         self.assertEqual(response.status_code, 201)
if __name__ == "__main__":
    unittest.main()
