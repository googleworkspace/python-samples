"""
Copyright 2019 Google LLC
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
# [START gmail_send_message_with_attachment]
from __future__ import print_function

import base64
import mimetypes
import os
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def gmail_send_message_with_attachment():
    """Create and send an email message with attachment
        Print the returned  message id
        Returns: Message object, including message id

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
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
        # encoded message
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()) \
            .decode()

        send_message_request_body = {
            'message': {

                'raw': encoded_message
            }
        }
        # pylint: disable=E1101
        send_message = (service.users().messages().send
                        (userId='me', body=send_message_request_body).execute())
        print(F'Message Id: {send_message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


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
    gmail_send_message_with_attachment()
# [END gmail_send_message_with_attachment]
