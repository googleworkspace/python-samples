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

    def test_update_signature(self):
        signature = self.snippets.update_signature()
        self.assertIsNotNone(signature)


if __name__ == '__main__':
    unittest.main()
