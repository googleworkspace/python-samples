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
# [START gmail_create_filter]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_filter():
    """Create a filter.
    Returns: Draft object, including filter id.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        label_name = 'IMPORTANT'
        filter_content = {
            'criteria': {
                'from': 'gsuder1@workspacesamples.dev'
            },
            'action': {
                'addLabelIds': [label_name],
                'removeLabelIds': ['INBOX']
            }
        }

        # pylint: disable=E1101
        result = service.users().settings().filters().create(
            userId='me', body=filter_content).execute()
        print(F'Created filter with id: {result.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        result = None

    return result.get('id')


if __name__ == '__main__':
    create_filter()
# [END gmail_create_filter]
