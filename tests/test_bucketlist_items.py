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
        self.assertEqual(rv.status_code, 201)
