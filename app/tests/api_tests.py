import unittest
import json
from base64 import b64encode

import app.models as models

import app


class ApiTests(unittest.TestCase):

    def setUp(self):
        app.app.config.from_object("config.TestingConfig")
        self.app = app.app.test_client()

        app.db.create_all()
        email = 'raddevon@gmail.com'
        password = '1234567'
        new_user = models.User(email, password, 'admin')
        app.db.session.commit()

        self.headers = {
            'Authorization': 'Basic ' + b64encode("{0}:{1}".format(email, password))
        }

    def tearDown(self):
        app.db.session.close()
        app.db.drop_all()

    # def testAddImage(self):
    #     self.app.get("/api/image")

    def testGetUserEmpty(self):
        response = self.app.get("/api/user/", headers=self.headers)
        print response.data
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()
