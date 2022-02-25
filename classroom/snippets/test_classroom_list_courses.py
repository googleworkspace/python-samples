"""Unit test file for List course snippet"""

import unittest
import classroom_list_courses

"""
Unit test class for List course snippet
"""


class TestClassroomListCourses(unittest.TestCase):
    """Unit test class for List course snippet"""
    @classmethod
    def test_classroom_create_course(cls):
        course = classroom_list_courses.classroom_list_courses()
        cls.assertIsNotNone(cls, course)


if __name__ == "__main__":
    unittest.main()
