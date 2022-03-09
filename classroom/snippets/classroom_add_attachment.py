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
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# [START classroom_add_attachment]


def classroom_add_attachment(course_id, coursework_id, submission_id):
    """
    Adds attachment to existing course with specific course_id.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    request = {
        'addAttachments': [
            {'link': {'url': 'http://example.com/quiz-results'}},
            {'link': {'url': 'http://example.com/quiz-reading'}}
        ]
    }

    try:
        service = build('classroom', 'v1', credentials=creds)
        while True:
            coursework = service.courses().courseWork()
            coursework.studentSubmissions().modifyAttachments(
                courseId=course_id,
                courseWorkId=coursework_id,
                id=submission_id,
                body=request).execute()

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    # Put the course_id, coursework_id and submission_id of course in which
    # attachment needs to be added.
    classroom_add_attachment('course_id', 'coursework_id', "me")
# [END classroom_add_attachment]
