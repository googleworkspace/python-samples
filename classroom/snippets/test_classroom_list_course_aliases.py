"""
Copyright 2022 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import unittest

from base_test import BaseTest
from classroom_create_course import classroom_create_course
from classroom_list_course_aliases import classroom_list_course_aliases


class TestClassroomListCourseAliases(BaseTest):
  """Unit test class for List course aliases snippet"""

  def test_classroom_list_course_aliases(self):
    """Unit test method for List course snippet"""
    course = classroom_create_course()
    self.assertIsNotNone(course)
    self.delete_course_on_cleanup(course.get("id"))
    course_aliases = classroom_list_course_aliases(course.get("id"))
    self.assertIsNotNone(course_aliases)


if __name__ == "__main__":
  unittest.main()
