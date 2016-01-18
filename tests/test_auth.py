from test_base import BaseTestCase
import app.auth as auth
import json


class AuthenticationTestCase(BaseTestCase):
    """ Tests correct user authentication """

    # ENDPOINT: POST '/auth/register'
    def test_registration(self):
        """Tests for correct user registration """
        user = {'username': 'Adelle', 'password': 'Hello'}
        req = self.client().get('/auth/register')
        self.assertEqual(req.status_code, 200)
        req = self.client().post('/auth/register', data=user)
        self.assertEqual(req.status_code, 201)
        self.assertIn('registered successfully', req.data)
        # test for empty registration: respond with bad request
        rv = self.client().post('/auth/register')
        self.assertEqual(rv.status_code, 400)

    def test_user_already_exists(self):
        """Tests for the already existing user """
        user = {'username': 'Adelle', 'password': 'Hello'}
        req = self.client().get('/auth/register')
        req = self.client().post('/auth/register', data=user)
        self.assertEqual(req.status_code, 201)
        another_user = {'username': 'Adelle', 'password': 'Hello'}
        another_req = self.client().get('/auth/register')
        req = self.client().post('/auth/register', data=another_user)
        self.assertNotEqual(another_req.status_code, 201)

    # ENDPOINT: POST '/auth/login'
    def test_logging_in(self):
        """Tests correct user login """
        req = self.client().post('/auth/login', data=self.user)
        self.assertEqual(req.status_code, 200)
        self.assertIn(auth.SERVICE_MESSAGES['login'], req.data)
        rv = self.client().get('/auth/login')
        self.assertEqual(rv.status_code, 202)
        # test for invalid credentials: respond with unauthorized
        wrong_req = self.client().post(
            '/auth/login',
            data={'username': 'its-me', 'password': 'i have no idea'})
        self.assertEqual(wrong_req.status_code, 401)

    # ENDPOINT: GET '/auth/logout'
    def test_logging_out(self):
        """Test user correctly logging out"""
        get_res = self.client().post('/auth/login', data=self.user)
        get_res_json = json.loads(get_res.data)
        jwtoken = get_res_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwtoken)}
        logout_req = self.client().get('/auth/logout', headers=headers)
        self.assertIn(auth.SERVICE_MESSAGES['logout'], logout_req.data)

    def test_correct_token_generation(self):
        """Tests correct token generation"""
        rv = self.client().post(
            '/auth/login',
            data={'username': 'its-me', 'password': 'i have no idea'})
        res_json = json.loads(rv.data)
        jwtoken = res_json.get('token')
        self.assertIsNone(jwtoken)
