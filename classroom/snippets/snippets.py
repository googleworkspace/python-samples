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

from __future__ import print_function
from googleapiclient import errors
import json


class ClassroomSnippets(object):
    def __init__(self, service):
        self.service = service

    def create_course(self):
        """
        Creates a 10th Grade Biology course.
        """
        service = self.service
        # [START classroom_create_course]
        course = {
            'name': '10th Grade Biology',
            'section': 'Period 2',
            'descriptionHeading': 'Welcome to 10th Grade Biology',
            'description': """We'll be learning about about the
                         structure of living creatures from a
                         combination of textbooks, guest lectures,
                         and lab work. Expect to be excited!""",
            'room': '301',
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }
        course = service.courses().create(body=course).execute()
        print('Course created:', course.get('name'), course.get('id'))
        # [END classroom_create_course]

    def get_course(self):
        """
        Retrieves a classroom course by its id.
        """
        service = self.service
        # [START classroom_get_course]
        course_id = '123456'
        try:
            course = service.courses().get(id=course_id).execute()
            print('Course "{%s}" found.', course.get('name'))
        except errors.HttpError:
            error = json.loads(e.content).get('error')
            if(error.get('code') == 404):
                print('Course with ID "{%s}" not found.', course_id)
            else:
                raise
        # [END classroom_get_course]

    def list_courses(self):
        """
        Lists all classroom courses.
        """
        service = self.service
        # [START classroom_list_courses]
        courses = []
        page_token = None

        while True:
            response = service.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not courses:
            print('No courses found.')
        else:
            print('Courses:')
            for course in courses:
                print(course.get('name'), course.get('id'))
        # [END classroom_list_courses]

    def add_alias_new(self):
        """
        Creates a course with alias specification.
        """
        service = self.service
        # [START classroom_new_alias]
        alias = 'd:school_math_101'
        course = {
            'id': alias,
            'name': 'Math 101',
            'section': 'Period 2',
            'description': 'Course Description',
            'room': '301',
            'ownerId': 'me'
        }
        try:
            course = service.courses().create(
                body=course).execute()
        except errors.HttpError:
            print('Course Creation Failed')
        # [END classroom_new_alias]

    def add_alias_existing(self):
        """
        Adds alias to existing course.
        """
        service = self.service
        # [START classroom_existing_alias]
        courseId = '123456'
        alias = 'd:school_math_101'
        courseAlias = {
            'alias': alias
        }
        try:
            courseAlias = service.courses().aliases().create(
                courseId=courseId,
                body=courseAlias).execute()
        except errors.HttpError:
            print('Alias Creation Failed')
        # [END classroom_existing_alias]
