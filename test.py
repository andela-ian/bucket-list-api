from app import create_app
import unittest


class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        bucket_list_app = create_app()
        self.client = bucket_list_app.test_client(self)

    # Test endpoints

    # Ensure that correct login behaves correctly
    def test_correct_login(self):
        rv = self.client.post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
        self.assertEqual(rv.status_code, 200)

    # Ensure that logout behave correctly
    def test_logout(self):
        self.client.post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
        rv = self.client.get('/logout')
        self.assertEqual(rv.status_code, 200)


if __name__ == '__main__':
    unittest.main()
