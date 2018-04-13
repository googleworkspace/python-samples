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

# [START people_quickstart]
"""
Shows basic usage of the People API. Outputs the name 10 connections.
"""
from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# Setup the People API
SCOPES = 'https://www.googleapis.com/auth/contacts.readonly'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('people', 'v1', http=creds.authorize(Http()))

# Call the People API
print('List 10 connection names')
results = service.people().connections()
    .list(
        resourceName='people/me',
        pageSize=10,
        personFields='names,emailAddresses')
    .execute()
connections = results.get('connections', [])

for person in connections:
    names = person.get('names', [])
    if len(names) > 0:
        name = names[0].get('displayName')
        print(name)
# [END people_quickstart]
