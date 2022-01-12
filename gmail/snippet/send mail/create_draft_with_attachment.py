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

# [START gmail_create_draft_with_attachment]

from __future__ import print_function

import mimetypes
import os
import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


def gmailCreateDraftWithAttachment():
    """Create and insert a draft email with attachment.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.
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
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)
        mime_message = MIMEMultipart()
        mime_message['to'] = 'gduser1@workspacesamples.dev'
        mime_message['from'] = 'gduser2@workspacesamples.dev'
        mime_message['subject'] = 'sample with attachment'
        text_part = MIMEText('Hi, this is automated mail with attachment.'
                             'Please do not reply.')
        mime_message.attach(text_part)
        image_attachment = build_file_part(file='photo.jpg')
        mime_message.attach(image_attachment)
        encoded_message = base64.urlsafe_b64encode(mime_message.\
                        as_string().encode()).decode()

        create_draft_request_body = {
            'message': {
                'raw': encoded_message
            }
        }
        draft = service.users().drafts().create(userId="me",\
                        body=create_draft_request_body).execute()
        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
    return draft


def build_file_part(file):
    """Creates a MIME part for a file.

    Args:
      file: The path to the file to be attached.

    Returns:
      A MIME part that can be attached to a message.
    """
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        with open(file, 'rb'):
            msg = MIMEText('r', _subtype=sub_type)
    elif main_type == 'image':
        with open(file, 'rb'):
            msg = MIMEImage('r', _subtype=sub_type)
    elif main_type == 'audio':
        with open(file, 'rb'):
            msg = MIMEAudio('r', _subtype=sub_type)
    else:
        with open(file, 'rb'):
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    return msg


if __name__ == '__main__':
    gmailCreateDraftWithAttachment()
    # [END gmail_create_draft_with_attachment]
