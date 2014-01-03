import unittest
import json

import app.models as models

import app


class ApiTests(unittest.TestCase):

    def setUp(self):
        app.app.config.from_object("config.TestingConfig")
        self.app = app.app.test_client()

        new_user = models.User('raddevon@gmail.com', '1234567', 'admin')

        app.db.create_all()

    def tearDown(self):
        app.db.session.close()
        app.db.drop_all()

    # def testAddImage(self):
    #     self.app.get("/api/image")

    def testGetUserEmpty(self):
        response = self.app.get("/api/user/")
        print response.data
        self.assertEqual(response.headers["Content-Type"], "application/json")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, {})


if __name__ == "__main__":
    unittest.main()
