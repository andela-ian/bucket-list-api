from bucketlistapp.models import db, User
from bucketlistapp.app import create_app
import unittest
import os


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        bucketlist_app = create_app('instance.config.TestingConfig')
        self.user_data = {'username': 'john', 'password': 'oldman'}
        self.app = bucketlist_app
        self.client = bucketlist_app.test_client
        with bucketlist_app.app_context():
            db.create_all()
            user = User(**self.user_data)
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
            with self.app.app_context():
                db.session.remove()
                db.drop_all()
                # os.close(self.app.config.get('DB_FD'))
                os.unlink(self.app.config.get('DATABASE'))
