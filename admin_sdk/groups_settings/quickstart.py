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

# [START admin_sdk_groups_settings_quickstart]
"""
Shows basic usage of the Admin SDK Groups Settings API. Outputs a group's
settings identified by the group's email address.
"""
from __future__ import print_function
from apiclient.discovery import build, http
from httplib2 import Http
from oauth2client import file, client, tools
import StringIO
import random

import apiclient
from email import Utils
from email import MIMEText

# Setup the Admin SDK Groups Migration API
SCOPES = 'https://www.googleapis.com/auth/apps.groups.settings'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('groupssettings', 'v1', http=creds.authorize(Http()))

groupEmail = raw_input('Enter the email address of a Google Group in your domain: ')
try:
    results = service.groups().get(groupUniqueId=groupEmail,
        alt='json').execute()
    print(json.dumps(results, indent=4))
except:
    print('Unable to read group: {0}'.format(groupEmail))
    raise
# [END admin_sdk_groups_settings_quickstart]
