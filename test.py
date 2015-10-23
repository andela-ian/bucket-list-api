from models import db, User
from app import create_app
from auth import MESSAGES
import unittest
import os
import json


class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        self.user_data = {'username': 'john', 'password': 'oldman'}
        bucketlist_app = create_app('config.TestingConfig')
        self.app = bucketlist_app
        self.client = bucketlist_app.test_client
        with bucketlist_app.app_context():
            db.create_all()
            user = User(**self.user_data)
            db.session.add(user)
            db.session.commit()

    # Test endpoints

    # Ensure that correct login behaves correctly
    # ENDPOINT: POST '/login'
    def test_correct_login(self):
        rv = self.client().post(
            '/login',
            data=self.user_data
            )
        self.assertEqual(rv.status_code, 200)
        self.assertIn(MESSAGES['login'], rv.data)

    # Ensure that logout behave correctly
    # ENDPOINT: GET '/logout'
    def test_logout(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().get(
            '/logout',
            headers=headers)
        self.assertIn(MESSAGES["logout"], rv.data)

    # Ensure that user can retrieve his/her bucketlist items
    # ENDPOINT: GET '/bucketlists'
    def test_user_can_retrieve_bucketlist_items(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
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

        self.client().get('/logout')

    # Ensure user can create new bucketlist
    # ENDPOINT: POST '/bucketlists'
    def test_user_can_create_new_bucketlist(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        self.assertEqual(rv.status_code, 201)
        self.client().get('/logout')

    # Ensure user can get buckletlist by id
    # ENDPOINT: GET /bucketlists/<id>
    def test_user_can_get_bucketlist_by_id(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        rv = self.client().get(
            '/bucketlists/1',
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can update bucketlist by id
    # ENDPOINT: PUT /bucketlists/<id>
    def test_user_can_update_bucketlist_by_id(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {
            'Authorization': 'Bearer {0}'.format(jwt_token),
        }
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        rv = self.client().put(
            '/bucketlists/1',
            data={'name': 'Witness the change'},
            headers=headers)
        self.assertEqual(rv.status_code, 200)

    # Ensure user can delete bucketlist by id
    # ENDPOINT: DELETE /bucketlist/<id>
    def test_user_can_delete_bucketlist_by_id(self):
        resp = self.client().post(
            '/login',
            data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {
            'Authorization': 'Bearer {0}'.format(jwt_token),
        }
        self.client().post(
            '/bucketlists',
            data={'name': 'Witness a miracle'}, headers=headers)
        rv = self.client().delete(
            '/bucketlists/1',
            headers=headers)
        self.assertEqual(rv.status_code, 410)

    # Ensure user can create new bucketlist item
    # ENDPOINT: POST /bucketlists/<id>/items
    def test_user_can_create_new_bucketlist_item(self):
        resp = self.client().post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
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
        resp = self.client().post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
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
        resp = self.client().post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
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
        resp = self.client().post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
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
        self.assertEqual(rv.status_code, 410)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            # os.close(self.app.config.get('DB_FD'))
            os.unlink(self.app.config.get('DATABASE'))

if __name__ == '__main__':
    unittest.main()
