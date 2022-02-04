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
# [START classroom_create_course]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_create_course():

    """
    Creates the courses the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """

    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member

    try:
        service = build('classroom', 'v1', credentials=creds)
        course = {
            'name': '10th Grade Mathematics Probability-2',
            'section': 'Period 3',
            'descriptionHeading': 'Welcome to 10th Grade Mathematics',
            'description': """We'll be learning about about the
                                 polynomials from a
                                 combination of textbooks and guest lectures.
                                 Expect to be excited!""",
            'room': '302',
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }
        # pylint: disable=maybe-no-member
        course = service.courses().create(body=course).execute()
        print(f"Course created:  {(course.get('name'), course.get('id'))}")
        return course

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    classroom_create_course()
# [END classroom_create_course]
