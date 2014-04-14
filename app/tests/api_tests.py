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
            'Authorization': 'Basic ' + b64encode('{0}:{1}'.format(self.admin_email, self.admin_password)),
            "Accept": "application/json"
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
            '/api/user/', data=json.dumps({'email': 'test@gmail.com', 'password': '1234567'}), headers=self.auth_headers, content_type="application/json")
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(response.status_code, 201)

    def testAddUserWithRole(self):
        response = self.app.post(
            '/api/user/', data=json.dumps({'email': 'test@gmail.com', 'password': '1234567', 'roles': ['admin']}), headers=self.auth_headers, content_type="application/json")
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertIn('admin', user.roles)
        self.assertEqual(response.status_code, 201)

    def testAddUserWithMultipleRoles(self):
        user_role = perms_models.Role('user')
        app.db.session.add(user_role)
        app.db.session.commit()
        roles = ['admin', 'user']
        response = self.app.post(
            '/api/user/', data=json.dumps({'email': 'test@gmail.com', 'password': '1234567', 'roles': roles}), headers=self.auth_headers, content_type="application/json")
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertItemsEqual(roles, user.roles)
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
        user_changes = json.dumps({'email': 'end@mail.com',
                                   'password': '7654321', 'roles': ['user', 'admin']})
        response = self.app.put(
            '/api/user/' + str(new_user.id), data=user_changes, headers=self.auth_headers, content_type="application/json")
        user = models.User.query.get(new_user.id)
        self.assertEqual(user.email, json.loads(user_changes)['email'])
        self.assertTrue(
            user.check_password(json.loads(user_changes)['password']))
        self.assertItemsEqual(
            user.roles, json.loads(user_changes)['roles'])


class RoleListApiTests(ApiTests):

    def testAddRole(self):
        response = self.app.post(
            '/api/role/', data=json.dumps({'name': 'test'}), headers=self.auth_headers)
        print "JSON dump: {}".format(json.dumps({'name': 'test'}))
        role = perms_models.Role.query.filter_by(name='test').first()
        self.assertIsNotNone(role)
        self.assertEqual(role.name, 'test')
        self.assertEqual(response.status_code, 201)

    def testGetRoles(self):
        roles = [perms_models.Role('writer'), perms_models.Role(
            'moderator'), perms_models.Role('editor')]
        for role in roles:
            app.db.session.add(role)
        app.db.session.commit()
        response = self.app.get('/api/role/', headers=self.auth_headers)
        returned_names = json.loads(response.data)
        role_names = [role.name for role in roles]
        self.assertIsNotNone(returned_names)
        self.assertItemsEqual(role_names, returned_names)
        self.assertEqual(response.status_code, 201)


if __name__ == "__main__":
    unittest.main()
