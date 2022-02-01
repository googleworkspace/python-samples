"""Copyright 2018 Google LLC

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
# [START gmail_enable_auto_reply]

from __future__ import print_function

from datetime import datetime, timedelta

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from numpy import long


def enable_auto_reply():
    """Enable auto reply.
    Returns:Draft object, including reply message and response meta data.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        start_time = (now - epoch).total_seconds() * 1000
        end_time = (now + timedelta(days=7) - epoch).total_seconds() * 1000
        vacation_settings = {
            'enableAutoReply': True,
            'responseBodyHtml': "I am on vacation and will reply when I am "
                                "back in the office. Thanks!",
            'restrictToDomain': True,
            'startTime': long(start_time),
            'endTime': long(end_time)
        }

        # pylint: disable=E1101
        response = service.users().settings().updateVacation(
            userId='me', body=vacation_settings).execute()
        print(F'Enabled AutoReply with message: '
              F'{response.get("responseBodyHtml")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        response = None

    return response


if __name__ == '__main__':
    enable_auto_reply()
# [END gmail_enable_auto_reply]
