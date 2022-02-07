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
# [START gmail_enable_forwarding]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def enable_forwarding():
    """Enable email forwarding.
    Returns:Draft object, including forwarding id and result meta data.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        address = {'forwardingEmail': 'gduser1@workspacesamples.dev'}

        # pylint: disable=E1101
        result = service.users().settings().forwardingAddresses(). \
            create(userId='me', body=address).execute()
        if result.get('verificationStatus') == 'accepted':
            body = {
                'emailAddress': result.get('forwardingEmail'),
                'enabled': True,
                'disposition': 'trash'
            }
            # pylint: disable=E1101
            result = service.users().settings().updateAutoForwarding(
                userId='me', body=body).execute()
            print(F'Forwarding is enabled : {result}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        result = None

    return result


if __name__ == '__main__':
    enable_forwarding()
# [END gmail_enable_forwarding]
