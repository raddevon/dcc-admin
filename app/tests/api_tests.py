import unittest
import json
from base64 import b64encode

import app.models as models
from flask.ext.permissions.models import Role

import app


class ApiTests(unittest.TestCase):

    def setUp(self):
        app.app.config.from_object("config.TestingConfig")
        self.app = app.app.test_client()

        app.db.create_all()
        admin_role = Role('admin')
        app.db.session.add(admin_role)
        app.db.session.commit()
        email = 'raddevon@gmail.com'
        password = '1234567'
        new_user = models.User(email, password, 'admin')
        app.db.session.add(new_user)
        app.db.session.commit()

        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(email, password))
        }

    def tearDown(self):
        app.db.session.close()
        app.db.drop_all()

    def testInitialUser(self):
        response = self.app.get("/api/user/", headers=self.headers)
        print response.data
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(
            data.itervalues().next()['email'], 'raddevon@gmail.com')
        self.assertEqual(len(data), 1)

    def testAddUser(self):
        response = self.app.post(
            '/api/user/', data={'email': 'test@gmail.com', 'password': '1234567'}, headers=self.headers)
        user = models.User.query.filter_by(email='test@gmail.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@gmail.com')
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()
