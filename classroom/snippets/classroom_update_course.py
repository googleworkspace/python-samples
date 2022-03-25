"""
Copyright 2018 Google LLC

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

# [START classroom_update_course]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_update_course(course_id):
    """
    Updates the courses names the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # pylint: disable=maybe-no-member

    creds, _ = google.auth.default()

    try:
        service = build('classroom', 'v1', credentials=creds)

        # Updates the section and room of Google Classroom.
        course = service.courses().get(id=course_id).execute()
        course['name'] = '10th Grade Physics - Light'
        course['section'] = 'Period 4'
        course['room'] = '410'
        course = service.courses().update(id=course_id, body=course).execute()
        print(f" Updated Course is:  {course.get('name')}")
        return course

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the course_id of course whose course needs to be updated.
    classroom_update_course('course_id')

# [END classroom_update_course]
