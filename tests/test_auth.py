from test_base import BaseTestCase
import app.auth as auth
import json
import unittest


class AuthTestCase(BaseTestCase):
    """ Tests correct user authentication """

    # ENDPOINT: POST '/auth/register'
    def test_registration(self):
        user = {'username': 'Adelle', 'password': 'Hello'}
        req = self.client().get('/auth/register')
        self.assertEqual(req.status_code, 200)
        req = self.client().post('/auth/register', data=user)
        self.assertEqual(req.status_code, 201)
        self.assertIn('registered successfully', req.data)

    # ENDPOINT: POST '/auth/login'
    def test_logging_in(self):
        req = self.client().post('/auth/login', data=self.user)
        self.assertEqual(req.status_code, 200)
        self.assertIn(auth.SERVICE_MESSAGES['login'], req.data)

    # ENDPOINT: GET '/auth/logout'
    def test_logging_out(self):
        get_res = self.client().post('/auth/login', data=self.user)
        get_res_json = json.loads(get_res.data)
        jwtoken = get_res_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        logout_req = self.client().get('/auth/logout', headers=headers)
        self.assertIn(auth.SERVICE_MESSAGES['logout'], logout_req.data)

if __name__ == '__main__':
    unittest.main()
