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

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# [START classroom_new_alias]

SCOPES = ['https://www.googleapis.com/auth/classroom.courses']


def classroom_add_alias_new():
    """
        Creates a course with alias specification the user has access to.
        The file token.json stores the user's access and refresh tokens, and is
        created automatically when the authorization flow completes for
        the first time.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity for
         guides on implementing OAuth2 for the application.
    """
    # pylint: disable=maybe-no-member
    creds = None
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

    alias = 'd:school_physics_333'
    course = {
        'id': alias,
        'name': 'English',
        'section': 'Period 2',
        'description': 'Course Description',
        'room': '301',
        'ownerId': 'me'
    }
    try:
        print('-------------')
        service = build('classroom', 'v1', credentials=creds)
        course = service.courses().create(body=course).execute()
        print('====================================')

    except HttpError as error:
        print('An error occurred: %s' % error)
    return course


if __name__ == '__main__':
    # pylint: disable=too-many-arguments
    # Put the course_id of course whose alias needs to be created.
    classroom_add_alias_new()

# [END classroom_new_alias]
