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
        # TODO - Capture output and assert
        threads.show_chatty_threads(self.service)


if __name__ == '__main__':
    unittest.main()
