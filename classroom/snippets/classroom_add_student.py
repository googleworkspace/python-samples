"""Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

# [START classroom_add_teacher]
from __future__ import print_function

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.students']


def classroom_add_student_new(course_id):
    """
    Adds a student to a course, the teacher has access to.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity for
     guides on implementing OAuth2 for the application.
     """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w', encoding="utf8") as token:
            token.write(creds.to_json())

    enrollment_code = 'abc-def'
    student = {
            'userId': 'gduser1@workspacesamples.dev'
        }
    try:
        service = build('classroom', 'v1', credentials=creds)
        student = service.courses().students().create(
                courseId=course_id,
                enrollmentCode=enrollment_code,
                body=student).execute()
        print(
                '''User {%s} was enrolled as a student in
                   the course with ID "{%s}"'''
                % (student.get('profile').get('name').get('fullName'),
                   course_id))
        return student
    except HttpError as error:
        print(error)
        return error


if __name__ == '__main__':
    # Put the course_id of course for which student needs to be added.
    classroom_add_student_new(478800920837)
# [END classroom_add_teacher]
