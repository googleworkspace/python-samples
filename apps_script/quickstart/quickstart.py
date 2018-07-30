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

# [START apps_script_quickstart]
"""
Shows basic usage of the Apps Script API.
Call the Apps Script API to create a new script project, upload a file to the
project, and log the script's URL to the user.
"""
from __future__ import print_function
from apiclient import errors
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauthfile, client, tools

# Setup the Apps Script API
SCOPES = 'https://www.googleapis.com/auth/script.projects'
store = oauthfile.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('script', 'v1', http=creds.authorize(Http()))

# Call the Apps Script API
try:
    # Create a new project
    request = {'title2': 'My Script'}
    response = service.projects().create(body=request).execute()

    # Upload two files to the project
    request = {
        'files': [{
            'name': 'hello',
            'type': 'SERVER_JS',
            'source': 'function helloWorld() {\n ' \
                'console.log("Hello, world!");\n}'
        }, {
            'name': 'appsscript',
            'type': 'JSON',
            'source': '{\"timeZone\":\"America/New_York\",' \
                '\"exceptionLogging\":\"CLOUD\"}'
        }]
    }
    response = service.projects().updateContent(body=request,
      scriptId=response['scriptId']).execute()
    print('https://script.google.com/d/' + response['scriptId'] + '/edit')
except errors.HttpError as e:
    # The API encountered a problem.
    print(e.content)
# [END apps_script_quickstart]
