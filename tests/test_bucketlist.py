from base_testcase import BaseTestCase
import json


class BucketListTestCase(BaseTestCase):

    # Ensure that user can retrieve his/her bucketlist items
    # ENDPOINT: GET '/bucketlists'
    def test_user_can_retrieve_bucketlist_items(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().get('/bucketlists', headers=headers)
        self.assertEqual(rv.status_code, 404)

        # write a bucket list and fetch
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        rv = self.client().get('/bucketlists', headers=headers)
        self.assertIn('Witness a miracle', rv.data)

        self.client().get('/auth/logout', headers=headers)

    # Ensure user can create new bucketlist
    # ENDPOINT: POST '/bucketlists'
    def test_user_can_create_new_bucketlist(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        self.client().get('/auth/logout', headers=headers)

    # Ensure user can get buckletlist by id
    # ENDPOINT: GET /bucketlists/<id>
    def test_user_can_get_bucketlist_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().get(
            '/bucketlists/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can update bucketlist by id
    # ENDPOINT: PUT /bucketlists/<id>
    def test_user_can_update_bucketlist_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {
            'Authorization': 'Bearer {0}'.format(jwt_token),
        }
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/bucketlists/1',
            data={'name': 'Witness the change'},
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can delete bucketlist by id
    # ENDPOINT: DELETE /bucketlist/<id>
    def test_user_can_delete_bucketlist_by_id(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {
            'Authorization': 'Bearer {0}'.format(jwt_token),
        }
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().delete(
            '/bucketlists/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)
