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

# [START admin_sdk_licensing_quickstart]
"""
Shows basic usage of the Admin SDK Licensing API. Outputs the first 10 license
assignments for G Suite seats.
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

# Setup the Admin SDK Licensing API
SCOPES = 'https://www.googleapis.com/auth/apps.licensing'
store = file.Storage('credentials.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('licensing', 'v1', http=creds.authorize(Http()))

customerId = raw_input('Enter the domain name of your G Suite domain: ')
results = service.licenseAssignments().listForProduct(
    productId='Google-Apps', customerId=customerId, maxResults=10).execute()
items = results.get('items', [])
if not items:
    print('No license assignments found.')
else:
    print('License assignments:')
    for item in items:
        print('{0} ({1})'.format(item['userId'], item['skuId']))
# [END admin_sdk_licensing_quickstart]
