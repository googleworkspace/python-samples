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

# [START classroom_list_courses]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_list_courses():

    """
    Prints the list of the courses the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

    creds, _ = google.auth.default()
    try:
        service = build('classroom', 'v1', credentials=creds)
        courses = []
        page_token = None

        while True:
            # pylint: disable=maybe-no-member
            response = service.courses().list(pageToken=page_token,
                                              pageSize=100).execute()
            courses.extend(response.get('courses', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not courses:
            print("No courses found.")
            return
        print("Courses:")
        for course in courses:
            print(f"{course.get('name'), course.get('id')}")
        return courses
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    print('Courses available are-------')
    classroom_list_courses()

# [END classroom_list_courses]
