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


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# [START classroom_patch_course]


def classroom_patch_course(course_id):
    """Shows basic usage of the Classroom API.
    Patch new course with existing course in the account the
    user has access to.
    """
    creds, _ = google.auth.default()

    # pylint: disable=maybe-no-member

    try:
        service = build('classroom', 'v1', credentials=creds)
        """ Creates a course with alias specification. """
        course = {
            'section': 'Period 3',
            'room': '313'
        }
        course = service.courses().patch(id=course_id,
                                         updateMask='section,room',
                                         body=course).execute()
        print('Course "%s" updated.' % course.get('name'))

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    # course_id1 = (classroom_update_course.classroom_list_courses())
    classroom_patch_course(456090670671)

# [END classroom_patch_course]
