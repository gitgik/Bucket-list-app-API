from test_base import BaseTestCase
import json


class BucketListTestCase(BaseTestCase):
    """ Tests Users can access their bucketlist(s) """

    # ENDPOINT: GET '/bucketlists'
    def test_user_can_get_bucketlist_items(self):
        login_res = self.client().post('/auth/login', data=self.user)
        login_data = json.loads(login_res.data)
        jwt_token = login_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().get('/bucketlists', headers=headers)
        self.assertEqual(rv.status_code, 404)

        # create a bucketlist and fetch it
        self.client().post('/bucketlists', data={'name': 'Swallow a python'},
                           headers=headers)
        rv = self.client().get('/bucketlists', headers=headers)
        self.assertIn('Swallow a python', rv.data)

    # ENDPOINT: POST '/bucketlists'
    def test_user_can_create_bucketlist(self):
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        self.client().get('/auth/logout', headers=headers)

