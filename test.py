from app import create_app
import unittest


class BucketListTestCase(unittest.TestCase):

    def setUp(self):
        bucketlist_app = create_app()
        self.client = bucketlist_app.test_client(self)

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

    # Ensure that user can retrieve his/her bucketlist items
    def test_user_can_retrieve_bucketlist_items(self):
        self.client.post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
        rv = self.client.get('/bucketlist')
        self.assertIn("No bucketlist items were found", rv.data)
        self.client.get('/logout')

    # Ensure user can create new bucketlist item
    def test_user_can_create_new_bucketlist_item(self):
        self.client.post(
            '/login',
            data={'username': 'john', 'password': 'oldman'}
            )
        rv = self.client.post(
            '/bucketlist',
            data={'todo': 'Witness a miracle'})
        self.assertEqual(rv.status_code, 201)
        self.client.get('/logout')

if __name__ == '__main__':
    unittest.main()
