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
# [START classroom_create_coursework]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_create_coursework(course_id):

    """
    Creates the coursework the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """

    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member

    try:
        service = build('classroom', 'v1', credentials=creds)
        coursework = {
            'title': 'Ant colonies',
            'description': '''Read the article about ant colonies
                              and complete the quiz.''',
            'materials': [
                {'link': {'url': 'http://example.com/ant-colonies'}},
                {'link': {'url': 'http://example.com/ant-quiz'}}
            ],
            'workType': 'ASSIGNMENT',
            'state': 'PUBLISHED',
        }
        coursework = service.courses().courseWork().create(
            courseId=course_id, body=coursework).execute()
        print(f"Assignment created with ID {coursework.get('id')}")
        return coursework

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the course_id of course whose coursework needs to be created,
    # the user has access to.
    classroom_create_coursework(453686957652)
# [END classroom_create_coursework]
