import unittest

import threads
from base_test import BaseTest

class ThreadsTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super(ThreadsTest, cls).setUpClass()

    def setUp(self):
        super(ThreadsTest, self).setUp()

    def tearDown(self):
        super(ThreadsTest, self).tearDown()


    def test_show_chatty_threads(self):
        threads = threads.show_chatty_threads(self.service)
        self.assertIsNotNone(threads) # Weak assertion

if __name__ == '__main__':
    unittest.main()
