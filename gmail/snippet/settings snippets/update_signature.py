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
# [START gmail_update_signature]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def update_signature():
    """Create and update signature in gmail.
    Returns:Draft object, including updated signature.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        primary_alias = None

        # pylint: disable=E1101
        aliases = service.users().settings().sendAs().list(userId='me')\
            .execute()
        for alias in aliases.get('sendAs'):
            if alias.get('isPrimary'):
                primary_alias = alias
                break

        send_as_configuration = {
            'displayName': primary_alias.get('sendAsEmail'),
            'signature': 'Automated Signature'
        }

        # pylint: disable=E1101
        result = service.users().settings().sendAs() \
            .patch(userId='me', sendAsEmail=primary_alias.get('sendAsEmail'),
                   body=send_as_configuration).execute()
        print(F'Updated signature for: {result.get("displayName")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        result = None

    return result.get('signature')


if __name__ == '__main__':
    update_signature()
# [END gmail_update_signature]
