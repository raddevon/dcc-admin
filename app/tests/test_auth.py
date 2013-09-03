import subprocess
import signal
import os
import sys
import time
import logging
import requests
from flask import Flask
from flask.ext.testing import TestCase
from selenium import webdriver
from app.models import db, User

app = Flask(__name__)
app.config['TESTING'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'


class TestAuth(TestCase):

    def create_app(self):
        db.init_app(app)
        return app

    @classmethod
    def setUpClass(cls):
        cls.server_proc = subprocess.Popen(
            [sys.executable, 'run.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        time.sleep(5)

    @classmethod
    def TearDownLcass(cls):
        os.kill(cls.server_proc.pid, signal.SIGINT)

    def setUp(self):
        selenium_logger = logging.getLogger(
            'selenium.webdriver.remote.remote_connection')
        selenium_logger.setLevel(logging.WARN)
        self.browser = webdriver.Firefox()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.browser.quit()

    def test_user_signup(self):
        self.browser.get('http://localhost:5000/signup')

    def test_user_login(self):
        pass


class TestDatabase(TestCase):

    def create_app(self):
        db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_saving_user_to_database(self):
        user = User('email@domain.com', '12345678')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.id, 1)

    def test_user_gets_default_role(self):
        user = User('email@domain.com', '12345678')
        db.session.add(user)
        db.session.commit()
        role_list = [role for role in user.roles]
        self.assertEqual(role_list[0].name, 'user')
