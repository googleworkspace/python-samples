import unittest

from base_test import BaseTest
from settings_snippets import SettingsSnippets


class SettingsSnippetsTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(SettingsSnippetsTest, cls).setUpClass()
        cls.snippets = SettingsSnippets(cls.service)

    def setUp(self):
        super(SettingsSnippetsTest, self).setUp()

    def tearDown(self):
        super(SettingsSnippetsTest, self).tearDown()

    def test_update_signature(self):
        signature = self.snippets.update_signature()
        self.assertIsNotNone(signature)


if __name__ == '__main__':
    unittest.main()
