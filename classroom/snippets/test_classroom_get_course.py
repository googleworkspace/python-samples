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

import classroom_create_course
import classroom_get_course
from base_test import BaseTest


class TestClassroomGetCourse(BaseTest):
    """Unit test class for Get course snippet"""
    def test_classroom_get_course(self):
        """Unit test method for Get course snippet"""
        course = classroom_create_course.classroom_create_course()
        self.assertIsNotNone(course)
        self.delete_course_on_cleanup(course.get('id'))
        course_id = classroom_get_course.classroom_get_course(course.get(
                    'id'))
        self.assertIsNotNone(course_id)


if __name__ == "__main__":
    unittest.main()
