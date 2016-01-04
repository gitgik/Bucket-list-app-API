from app.models import db, User
from app.app import create_app
import os
import unittest


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        bucket_app = create_app('instance.config.TestingConfig')
        self.user = {'username': 'its-me', 'password': '1234'}
        self.app = bucket_app
        self.client = self.app.test_client
        with bucket_app.app_context():
            db.create_all()
            user = User(**self.user)
            user.save()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            os.unlink(self.app.config.get('DATABASE'))

if __name__ == '__main__':
    unittest.main()
