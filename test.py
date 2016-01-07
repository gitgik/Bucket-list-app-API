from tests import test_auth, test_bucketlist, test_bucketlist_items
import unittest

suite = unittest.TestLoader().loadTestsFromTestCase(
    test_auth.AuthenticationTestCase)
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
    test_bucketlist.BucketListTestCase))
suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
    test_bucketlist_items.BucketListItemTestCase))

unittest.TextTestRunner(verbosity=2).run(suite)
