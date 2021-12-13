
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

from base_test import BaseTest
from classroom_snippets import ClassroomSnippets


class SnippetsTest(BaseTest):

    @classmethod
    def setUpClass(cls):
        super(SnippetsTest, cls).setUpClass()
        cls.snippets = ClassroomSnippets(cls.service)

    def test_create_course(self):
        course = self.snippets.create_course()
        self.assertIsNotNone(course)
        self.delete_course_on_cleanup(course.get('id'))


if __name__ == '__main__':
    unittest.main()
