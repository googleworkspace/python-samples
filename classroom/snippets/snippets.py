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

class ClassroomSnippets(object):
    def __init__(self, service):
        self.service = service    

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
        except:
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
        except:
            print('Alias Creation Failed')
        # [END classroom_existing_alias]
