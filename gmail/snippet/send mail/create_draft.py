# Copyright 2019 Google LLC
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

# [START gmail_create_draft]

from __future__ import print_function
import os
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES =['https://www.googleapis.com/auth/gmail.compose	']


def gmailCreateDraft():
    """Create and insert a draft email.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.
    """
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file \
                ('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w', encoding='UTF') as token:
            token.write(creds.to_json())

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        message = MIMEText('This is automated draft mail')
        message['to'] = 'gduser1@workspacesamples.dev'
        message['from'] = 'gduser2@workspacesamples.dev'
        message['subject'] = 'Automated draft'
        encoded_message = base64.urlsafe_b64encode\
            (message.as_string().encode()).decode()

        create_message = {
            'message': {
                'raw' : encoded_message
            }
        }
        draft = service.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
    return draft


if __name__ == '__main__':
    gmailCreateDraft()
# [END gmail_create_draft]
