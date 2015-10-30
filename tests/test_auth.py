from base_testcase import BaseTestCase
from bucketlistapp.auth import MESSAGES
import json


class AuthTestCase(BaseTestCase):

    # Test endpoints

    # Ensure that user can register correctly
    # ENDPOINT: POST '/auth/register'
    def test_user_can_register(self):
        user_data = {'username': 'Methuselah', 'password': 'very_old'}
        rv = self.client().get('/auth/register')
        self.assertEqual(rv.status_code, 200)
        rv = self.client().post('/auth/register', data=user_data)
        self.assertEqual(rv.status_code, 201)
        self.assertIn("registered successfully", rv.data)

    # Ensure that user can login
    # ENDPOINT: POST '/auth/login'
    def test_user_can_login(self):
        rv = self.client().post('/auth/login', data=self.user_data)
        self.assertEqual(rv.status_code, 200)
        self.assertIn(MESSAGES['login'], rv.data)

    # Ensure that logout behave correctly
    # ENDPOINT: GET '/auth/logout'
    def test_user_can_logout(self):
        resp = self.client().post('/auth/login', data=self.user_data)
        resp_json = json.loads(resp.data)
        jwt_token = resp_json.get('token')
        headers = {'Authorization': 'Bearer {0}'.format(jwt_token)}
        rv = self.client().get(
            '/auth/logout',
            headers=headers)
        self.assertIn(MESSAGES["logout"], rv.data)
