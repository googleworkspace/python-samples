"""
Copyright 2018 Google LLC

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

# [START people_quickstart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/contacts.readonly']


def main():
    """
    Shows basic usage of the People API.
    Prints the name of the first 10 connections.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    creds, _ = google.auth.default()

    try:
        service = build('people', 'v1', credentials=creds)

        # Call the People API
        # pylint: disable=no-member
        print('List 10 connection names')
        results = service.people().connections().list(
            resourceName='people/me',
            pageSize=10,
            personFields='names,emailAddresses').execute()
        connections = results.get('connections', [])

        for person in connections:
            names = person.get('names', [])
            if names:
                name = names[0].get('displayName')
                print(name)
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
# [END people_quickstart]
