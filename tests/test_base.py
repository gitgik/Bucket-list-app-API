from app.models import db, User
from app.app import create_app
import os
import unittest

class BaseTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app('instance.config.TestingConfig')
        self.user = {'username': 'its-me', 'password': '1234'}
        self.app = app
        self.client = app.test_client
        with app.app_context():
            db.create_all()
            user = User(**self.user_data)
            user.save()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(self.app.config.get('DATABASE'))