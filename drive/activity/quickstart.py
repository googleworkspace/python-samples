# Copyright 2018 Google LLC
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

# [START drive_activity_quickstart]
from __future__ import print_function

import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/activity']


def main():
    """Shows basic usage of the Drive Activity API.
    Prints information about the last 10 events that occured the user's Drive.
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
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('appsactivity', 'v1', credentials=creds)

    # Call the Drive Activity API
    results = service.activities().list(source='drive.google.com',
                                        drive_ancestorId='root', pageSize=10).execute()
    activities = results.get('activities', [])

    if not activities:
        print('No activity.')
    else:
        print('Recent activity:')
        for activity in activities:
            event = activity['combinedEvent']
            user = event.get('user', None)
            target = event.get('target', None)
            if user is None or target is None:
                continue
            time = datetime.datetime.fromtimestamp(
                int(event['eventTimeMillis']) / 1000)
            print(u'{0}: {1}, {2}, {3} ({4})'.format(time, user['name'],
                                                     event['primaryEventType'], target['name'], target['mimeType']))


if __name__ == '__main__':
    main()
# [END drive_activity_quickstart]
