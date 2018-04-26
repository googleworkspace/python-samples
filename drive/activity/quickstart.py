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
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/appsactivity-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/activity https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'G Suite Activity API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'appsactivity-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the G Suite Activity API.

    Creates a G Suite Activity API service object and
    outputs the recent activity in your Google Drive.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('appsactivity', 'v1', http=http)

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
            if user == None or target == None:
                continue
            time = datetime.datetime.fromtimestamp(
                int(event['eventTimeMillis'])/1000)
            print('{0}: {1}, {2}, {3} ({4})'.format(time, user['name'],
                event['primaryEventType'], target['name'], target['mimeType']))

if __name__ == '__main__':
    main()
# [END drive_activity_quickstart]
