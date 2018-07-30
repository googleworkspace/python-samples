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

# [START tasks_quickstart]
"""
Shows basic usage of the Tasks API. Outputs the first 10 task lists.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauthfile, client, tools

# Setup the Tasks API
SCOPES = 'https://www.googleapis.com/auth/tasks.readonly'
store = oauthfile.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('tasks', 'v1', http=creds.authorize(Http()))

# Call the Tasks API
results = service.tasklists().list(maxResults=10).execute()
items = results.get('items', [])
if not items:
    print('No task lists found.')
else:
    print('Task lists:')
    for item in items:
        print('{0} ({1})'.format(item['title'], item['id']))
# [END tasks_quickstart]
