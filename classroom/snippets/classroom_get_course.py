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

# [START classroom_get_course]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_get_course(course_id):

    """
    Prints the name of the with specific course_id.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    course = None
    try:
        service = build('classroom', 'v1', credentials=creds)
        course = service.courses().get(id=course_id).execute()
        print(f"Course found : {course.get('name')}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Course not found: {course_id}")
        return error
    return course


if __name__ == '__main__':
    # Put the course_id of course whose information needs to be fetched.
    classroom_get_course('course_id')

# [END classroom_get_courses]
