"""Unit test file for Get course snippet"""
import unittest
import classroom_get_course
import classroom_list_courses

"""
Unit test class for Get course snippet
"""


class TestClassroomGetCourse(unittest.TestCase):
    """Unit test class for Get course snippet"""
    @classmethod
    def test_classroom_get_course(cls):
        course = classroom_list_courses.classroom_list_courses()
        for i in course:
            course_id = classroom_get_course.classroom_get_course(course.
                                                                  get('id'))
            cls.assertIsNotNone(cls, course_id)
            break


if __name__ == "__main__":
    unittest.main()
