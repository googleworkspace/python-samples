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

# [START admin_sdk_groups_migration_quickstart]
"""
Shows basic usage of the Admin SDK Groups Migration API. Inserts a test email
into a group.
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
SCOPES = 'https://www.googleapis.com/auth/apps.groups.migration'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('groupsmigration', 'v1', http=creds.authorize(Http()))

# Call the Admin SDK Groups Migration API
print('Warning: A test email will be inserted into the group entered.')
groupId = raw_input(
    'Enter the email address of a Google Group in your domain: ')

# Format an RFC822 message
message = MIMEText.MIMEText('This is a test.')
# Generate a random 10 digit number for message Id.
message['Message-ID'] = '<{0}-{1}>'.format(str(random.randrange(10**10)),
                                           groupId)
message['Subject'] = 'Groups Migration API Test (Python)'
message['From'] = '"Alice Smith" <alice@example.com>'
message['To'] = groupId
message['Date'] = Utils.formatdate(localtime=True)

stream = StringIO.StringIO()
stream.write(message.as_string())
media = apiclient.http.MediaIoBaseUpload(stream,
                                         mimetype='message/rfc822')

result = service.archive().insert(groupId=groupId,
                                  media_body=media).execute()
print(result['responseCode'])
# [END admin_sdk_groups_migration_quickstart]
