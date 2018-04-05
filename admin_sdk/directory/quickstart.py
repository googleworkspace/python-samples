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

# [START admin_sdk_directory_quickstart]
"""
Shows basic usage of the Admin SDK Directory API. Lists of first 10 users in the
domain.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the Admin SDK Directory API
SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('admin', 'directory_v1', http=creds.authorize(Http()))

# Call the Admin SDK Directory API
print('Getting the first 10 users in the domain')
results = service.users().list(customer='my_customer', maxResults=10,
                               orderBy='email').execute()
users = results.get('users', [])

if not users:
    print('No users in the domain.')
else:
    print('Users:')
    for user in users:
        print('{0} ({1})'.format(user['primaryEmail'], user['name']['fullName']))
# [END admin_sdk_directory_quickstart]
