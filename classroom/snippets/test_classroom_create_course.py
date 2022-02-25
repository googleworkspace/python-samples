"""Unit test file for Create course snippet"""
import unittest
import classroom_create_course
"""
Unit test class for Create course snippet
"""


class TestClassroomCreateCourse(unittest.TestCase):
    @classmethod
    def test_classroom_create_course(cls):
        """Class function for Create course snippet"""
        course = classroom_create_course.classroom_create_course()
        cls.assertIsNotNone(cls, course)
        cls.doClassCleanups()


if __name__ == "__main__":
    unittest.main()
