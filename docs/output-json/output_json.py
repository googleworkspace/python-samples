# -*- coding: utf-8 -*-
#
# Copyright ©2018-2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
ouput-json.py (Python 2.x or 3.x)
Google Docs (REST) API output-json sample app
"""
# [START output_json_python]
from __future__ import print_function

import json

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set doc ID, as found at `https://docs.google.com/document/d/YOUR_DOC_ID/edit`
DOCUMENT_ID = "195j9eDD3ccgjQRttHhJPymLJUCOUjs-jmwTrekvdjFE"

# Set the scopes and discovery info
SCOPES = 'https://www.googleapis.com/auth/documents.readonly'
DISCOVERY_DOC = ('https://docs.googleapis.com/$discovery/rest?'
                 'version=v1')

# Initialize credentials and instantiate Docs API service
creds, _ = google.auth.default()
# pylint: disable=maybe-no-member
try:
    service = build('docs', 'v1', credentials=creds)

    # Do a document "get" request and print the results as formatted JSON

    result = service.documents().get(documentId=DOCUMENT_ID).execute()
    print(json.dumps(result, indent=4, sort_keys=True))
except HttpError as error:
    print(f"An error occurred: {error}")

# [END output_json_python]
