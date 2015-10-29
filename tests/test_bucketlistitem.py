from base_testcase import BaseTestCase
from faker import Faker
import json


class BucketListItemTestCase(BaseTestCase):

    # Ensure user can create new bucketlist item
    # ENDPOINT: POST /bucketlists/<id>/items
    def test_user_can_create_new_bucketlist_item(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        rv = self.client().post(
            '/bucketlists/1/items',
            data={'name': 'Water changes into wine'},
            headers=headers)
        self.assertEqual(rv.status_code, 201)

    # Ensure user can get new bucketlist item by item_id
    # ENDPOINT: GET /bucketlists/<id>/items/<item_id>
    def test_user_can_get_bucketlist_item_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.client().post(
            '/bucketlists/1/items',
            data={'name': 'Water changes into wine'},
            headers=headers)
        rv = self.client().get(
            '/bucketlists/1/items/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can update new bucketlist item by item_id
    # ENDPOINT: PUT /bucketlists/<id>/items/<item_id>
    def test_user_can_update_bucketlist_item_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.client().post(
            '/bucketlists/1/items',
            data={'name': 'Water changes into wine'},
            headers=headers)
        rv = self.client().put(
            '/bucketlists/1/items/1',
            data={'name': 'Reverse the time'},
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can delete new bucketlist item by item_id
    # ENDPOINT: DELETE /bucketlists/<id>/items/<item_id>
    def test_can_delete_bucketlist_item_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.client().post(
            '/bucketlists/1/items',
            data={'name': 'Water changes into wine'},
            headers=headers)
        rv = self.client().delete(
            '/bucketlists/1/items/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can gets 20 bucket list records up
    # to a maximum of 100 records paginated
    # ENDPOINT: GET /bucketlists?limit=20
    def test_can_get_bucket_list_records_up_to_a_hundred(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        faker = Faker()
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
                '/bucketlists',
                data={'name': 'Extreme Activities'}, headers=headers)
        for bucketeer in range(0, 100):
            self.client().post(
                '/bucketlists/1/items',
                data={'name': faker.catch_phrase()},
                headers=headers)
        rv = self.client().get('/bucketlists?limit=20', headers=headers)
        json_data = json.loads(rv.data)
        self.assertEqual(len(json_data['message']), 20)
        self.assertEqual(rv.status_code, 200)
        rv = self.client().get('/bucketlists?limit=1000', headers=headers)
        self.assertEqual(rv.status_code, 406)

    # Ensure user can search bucketlist
    # ENDPOINT: GET /bucketlists?q=bucket1
    def test_can_search_bucketlists(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        names = [
            "Extreme Action",
            "Extreme Activities",
            "Extreme Kill",
        ]
        for name in names:
            self.client().post(
                '/bucketlists',
                data={'name': name}, headers=headers)
        rv = self.client().get('/bucketlists?q=Extreme', headers=headers)
        json_data = json.loads(rv.data)
        self.assertEqual(len(json_data['message']), 3)
        self.assertEqual(rv.status_code, 200)
