from test_base import BaseTestCase
import json


class BucketListTestCase(BaseTestCase):
    """Tests various endpoints to a bucketlist """

    # ENDPOINT: GET '/bucketlists'
    def test_user_can_get_bucketlist_items(self):
        """Tests users can retrieve their bucketlists """
        login_res = self.client().post('/auth/login', data=self.user)
        login_data = json.loads(login_res.data)
        jwt_token = login_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().get('/bucketlists/', headers=headers)
        self.assertEqual(rv.status_code, 404)

        # create a bucketlist and fetch it
        self.client().post('/bucketlists/', data={'name': 'Swallow a python'},
                           headers=headers)
        rv = self.client().get('/bucketlists/', headers=headers)
        self.assertIn('Swallow a python', rv.data)
        # logout the user after testing
        self.client().get('/auth/logout', headers=headers)

    # ENDPOINT: GET /bucketlists/<id>
    def test_users_can_get_bucketlist_using_id(self):
        """Tests users can retrieve a bucketlist by specifying its id """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().get('bucketlists/1', headers=headers)
        self.assertEqual(rv.status_code, 200)
        self.assertIn('Eat pray and love', rv.data)

    # ENDPOINT: POST '/bucketlists'
    def test_user_can_create_bucketlist(self):
        """Tests users to create a new bucketlist """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertIn("bucketlist", rv.data)
        self.assertEqual(rv.status_code, 201)
        results = self.client().get('/bucketlists/1', headers=headers)
        self.assertIn('Eat pray and love', results.data)
        # logout the user after testing
        self.client().get('/auth/logout', headers=headers)

    # ENDPOINT: PUT /bucketlist/<id>
    def test_users_can_edit_bucketlist(self):
        """Tests users can edit an existing bucketlist by id"""
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={
                "name": "Dont just eat, but also pray and love :-)"
            },
            headers=headers)
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1', headers=headers)
        self.assertIn('Dont just eat', results.data)

    # ENDPOINT: DELETE: '/bucketlist/<id>'
    def test_users_can_delete_bucketlist(self):
        """Tests users can delete their bucketlist by id """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists/',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().delete('/bucketlists/1', headers=headers)
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/bucketlists/1', headers=headers)
        self.assertIn('No such bucketlist', results.data)

