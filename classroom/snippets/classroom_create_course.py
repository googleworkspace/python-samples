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

# [START classroom_main]
from __future__ import print_function

import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

# [START classroom_create_course]
def classroom_create_course():
    """Shows basic usage of the Classroom API.
    Creates the courses the user has access to.
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
        with open('token.json', 'w', encoding='UTF') as token:
            token.write(creds.to_json())

    try:
        service = build('classroom', 'v1', credentials=creds)
        course = {
            'name': '10th Grade Biology',
            'section': 'Period 2',
            'descriptionHeading': 'Welcome to 10th Grade Biology',
            'description': """We'll be learning about about the
                                 structure of living creatures from a
                                 combination of textbooks, guest lectures,
                                 and lab work. Expect to be excited!""",
            'room': '301',
            'ownerId': 'me',
            'courseState': 'PROVISIONED'
        }
        course = service.courses().create(body=course).execute()
        print(F'Course created: {course.get("name")}, {course.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
    return course


if __name__ == '__main__':
    classroom_create_course()
# [END classroom_create_course]
