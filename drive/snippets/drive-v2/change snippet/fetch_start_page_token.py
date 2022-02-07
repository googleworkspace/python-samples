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
# [START drive_fetch_start_page_token]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def fetch_start_page_token():
    """Retrieve page token for the current state of the account.
    Returns & prints : start page token
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v2', credentials=creds)

        # pylint: disable=maybe-no-member
        response = service.changes().getStartPageToken().execute()
        print(F'Start token: {response.get("startPageToken")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        response = None

    return response.get('startPageToken')


if __name__ == '__main__':
    fetch_start_page_token()
# [End drive_fetch_start_page_token]
