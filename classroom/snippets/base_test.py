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

import sys
import unittest

import httplib2
from googleapiclient import errors
from googleapiclient.discovery import build
from oauth2client.client import GoogleCredentials

SCOPES = 'https://www.googleapis.com/auth/classroom.courses'


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.credentials = cls.create_credentials()
        http = cls.credentials.authorize(httplib2.Http())
        cls.credentials.refresh(http)
        cls.service = build('classroom', 'v1', http=http)
        cls.stdout = sys.stdout
        sys.stdout = None

    @classmethod
    def tearDownClass(cls):
        # Restore STDOUT.
        sys.stdout = cls.stdout

    @classmethod
    def create_credentials(cls):
        cls.credentials = GoogleCredentials.get_application_default()
        scope = ['https://www.googleapis.com/auth/drive']
        return cls.credentials.create_scoped(scope)

    def setUp(self):
        self.courses_to_delete = []
        print("Meow" + str(self.courses_to_delete))

    def tearDown(self):
        for course_id in self.courses_to_delete:
            try:
                self.service.courses().delete(id=course_id).execute()
            except errors.HttpError:
                print('Unable to delete file %s' % course_id)

    def delete_course_on_cleanup(self, course_id):
        self.courses_to_delete.append(course_id)


if __name__ == '__main__':
    unittest.main()
