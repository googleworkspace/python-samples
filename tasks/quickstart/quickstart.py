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

# [START tasks_quickstart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks.readonly']


def main():
    """
    Shows basic usage of the Tasks API.
    Prints the title and ID of the first 10 task lists.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    # pylint: disable=no-member
    creds, _ = google.auth.default()

    try:
        service = build('tasks', 'v1', credentials=creds)

        # Call the Tasks API
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print('No task lists found.')
            return

        print('Task lists:')
        for item in items:
            print(f"'{0} ({1})'.{format(item['title'], item['id'])}")
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
# [END tasks_quickstart]
