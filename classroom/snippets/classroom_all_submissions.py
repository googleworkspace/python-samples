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

# [START classroom_all_submissions]


def classroom_all_submissions(course_id, user_id):
    """
    Creates the list of all submissions of the courses the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """

    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    submissions = []
    page_token = None

    try:
        service = build('classroom', 'v1', credentials=creds)
        while True:
            coursework = service.courses().courseWork()
            response = coursework.studentSubmissions().list(
                pageToken=page_token,
                courseId=course_id,
                courseWorkId="-",
                userId=user_id).execute()
            submissions.extend(response.get('studentSubmissions', []))
            page_token = response.get('nextPageToken', None)
            if not page_token:
                break

        if not submissions:
            print('No student submissions found.')
        else:
            print('Complete list of student Submissions:')
            for submission in submissions:
                print("%s was submitted at %s" %
                      (submission.get('id'),
                       submission.get('creationTime')))

    except HttpError as error:
        print(f"An error occurred: {error}")
        submissions = None
    return submissions


if __name__ == '__main__':
    # Put the course_id and user_id of course whose list needs to be
    # submitted.
    classroom_all_submissions(453686957652, 466086979658)
# [END classroom_all_submissions]
