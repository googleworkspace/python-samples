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
import base64
from email.mime.text import MIMEText
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmailCreateDraft():
    """Create and insert a draft email.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.
    """
    # Load pre-authorized user credentials from the environment.
    # TODO(developer) - See https://developers.google.com/identity for
    #  guides on implementing OAuth2 for the application.
    credentials, _=google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=credentials)

        message = MIMEText('This is automated draft mail')
        message['to'] = 'gduser1@workspacesamples.dev'
        message['from'] = 'gduser2@workspacesamples.dev'
        message['subject'] = 'Automated draft'
        # encoding
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
