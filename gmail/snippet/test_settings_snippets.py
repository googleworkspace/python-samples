# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

    def create_test_label(self):
        labels = self.service.users().labels().list(userId='me').execute()
        for label in labels.get('labels'):
            if label.get('name') == 'testLabel':
                return label

        body = {
            'name': 'testLabel',
            'labelListVisibility': 'labelShow',
            'messageListVisibility': 'show'
        }
        return self.service.users().labels().create(userId='me', body=body).execute()

    def test_update_signature(self):
        signature = self.snippets.update_signature()
        self.assertIsNotNone(signature)

    def test_create_filter(self):
        test_label = self.create_test_label()
        id = self.snippets.create_filter(test_label.get('id'))
        self.assertIsNotNone(id)
        self.service.users().settings().filters().delete(userId='me', id=id).execute()
        self.service.users().labels().delete(userId='me', id=test_label.get('id'))

    def test_enable_auto_forwarding(self):
        forwarding = self.snippets.enable_forwarding(BaseTest.FORWARDING_ADDRESS)
        self.assertIsNotNone(forwarding)
        body = {
            'enabled': False,
        }
        self.service.users().settings().updateAutoForwarding(userId='me', body=body).execute()
        self.service.users().settings().forwardingAddresses().delete(
            userId='me', forwardingEmail=BaseTest.FORWARDING_ADDRESS).execute()

    def test_enable_auto_reply(self):
        settings = self.snippets.enable_auto_reply()
        self.assertIsNotNone(settings)


if __name__ == '__main__':
    unittest.main()
