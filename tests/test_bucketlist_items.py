from test_base import BaseTestCase
from faker import Faker
import json


class TestBucketListItem(BaseTestCase):
    """Tests an actionable bucketlist and all items operations in it """

    # ENDPOINT: POST /bucketlists/<id>/items
    def test_user_can_create_new_bucketlist_item(self):
        """Tests users can create an item inside their bucketlist """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().post(
            '/bucketlists/1/items',
            data={"name": "Go to Osteria Francescana"},
            headers=headers)
        self.assertEqual(rv.status_code, 201)

    def test_user_can_retrieve_bucketlist_items(self):
        """Tests users can retrieve a bucketlist item by id """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().get(
            '/bucketlists/1/items',
            data={"name": "Go to Osteria Francescana and dine lavishly"},
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # ENDPOINT: DELETE: '/bucketlists/<id>/items/<item_id>'
    def tests_user_can_delete_bucketlist_item(self):
        """Tests users can delete a bucketlist item by id """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Eat pray and love'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().get(
            '/bucketlists/1/items',
            data={"name": "Go to Osteria Francescana and dine lavishly"},
            headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().delete(
            '/bucketlists/1/items/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    def test_user_can_search_bucketlists(self):
        """Tests users can search for an existing bucketlist """
        res = self.client().post('/auth/login', data=self.user)
        res_data = json.loads(res.data)
        jwt_token = res_data.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}

        names = [
            "Become a pythonista",
            "Go out for a party",
            "Make a drone",
            "Make a comeback",
        ]
        for name in names:
            self.client().post(
                '/bucketlists',
                data={"name": name},
                headers=headers)
        # search for a bucketlist starting with "Make"
        rv = self.client().get('/bucketlists?q=Make', headers=headers)
        self.assertEqual(rv.status_code, 200)
        results_data = json.loads(rv.data)
        results_length = len(results_data['message'])
        self.assertEqual(results_length, 2)
