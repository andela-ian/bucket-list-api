from app import app
import unittest


class BucketListTestCase(unittest.TestCase):
    
    def setUp(self):
        self.client = app.test_client(self)

    # Test endpoints
    
    # Ensure that login loads correctly
    def test_login_loads(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
    
    # Ensure that correct login behaves correctly 
    def test_correct_login(self):
        response = self.client.get('/login')
        self.assertTrue(response.status_code == 200)
        response = self.client.post('/login', {username:'john', password:'oldman'}, follow_redirects=True)
        self.assertTrue(response.status_code == 200)
    
    # Ensure that logout behave correctly
    def test_logout(self):
        self.client.post('/login', {username:'john', password:'oldman'})
        response = self.client.get('/logout', follow_redirects=True)
        self.assertTrue(response.status_code == 200)


 if __name__ == '__main__':
     unittest.main()
