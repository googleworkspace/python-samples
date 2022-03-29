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

# [START vault_quickstart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/ediscovery']


def main():
    """
    Shows basic usage of the Vault API.
    Prints the names and IDs of the first 10 matters in Vault.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    creds, _ = google.auth.default()

    try:

        service = build('vault', 'v1', credentials=creds)

        # Call the Vault API
        # pylint: disable=no-member
        results = service.matters().list(pageSize=10).execute()
        matters = results.get('matters', [])

        if not matters:
            print('No matters found.')
            return

        print('Matters:')
        for matter in matters:
            print(f"(Matter is:)"
                  f".{format(matter.get('name'), matter.get('id'))}")
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
# [END vault_quickstart]
