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

# [START admin_sdk_reports_quickstart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/admin.reports.audit.readonly']


def main():
    """
    Shows basic usage of the Admin SDK Reports API.
    Prints the time, email, and name of the last 10 login events in the domain.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    creds, _ = google.auth.default()

    service = build('admin', 'reports_v1', credentials=creds)

    # Call the Admin SDK Reports API
    # pylint: disable=no-member
    print('Getting the last 10 login events')
    results = service.activities().list(userKey='all', applicationName='login',
                                        maxResults=10).execute()
    activities = results.get('items', [])

    if not activities:
        print('No logins found.')
    else:
        print('Logins:')
        for activity in activities:
            print(f'{0}: {1} ({2})'.format(activity['id']['time'],
                                           activity['actor']['email'],
                                           activity['events'][0]['name']))


if __name__ == '__main__':
    main()
# [END admin_sdk_reports_quickstart]
