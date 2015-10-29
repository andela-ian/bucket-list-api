from tests import *
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    test_auth.AuthTestCase)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
    test_bucketlist.BucketListTestCase))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
    test_bucketlistitem.BucketListItemTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)
