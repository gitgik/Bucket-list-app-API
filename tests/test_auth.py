import unittest
from test_base import BaseTestCase
from app.config import TestingConfig
import app.auth as auth
import json

class AuthTestCase(BaseTestCase):
    """ Tests correct user authentication """

    # ENDPOINT: POST /auth/register
    def test_registration(self):
        app = create_app(TestingConfig)
        self.client = app.test_client
        user = {'username':'Adelle', 'password':'Hello'}
        req = self.client().get('/auth/register')
        self.assertEqual(req.status_code, 200)
        req = self.client().post('/auth/register', data=user)
        self.assertEqual(req.status_code, 201)
        self.assertIn('registered successfully', req.data)

