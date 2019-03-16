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
docs-mail-merge.py (Python 2.x or 3.x)

Google Docs (REST) API mail-merge sample app
"""
# [START mail_merge_python]
from __future__ import print_function
import time

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# Fill-in IDs of your Docs template & any Sheets data source
DOCS_FILE_ID = 'YOUR_TMPL_DOC_FILE_ID'
SHEETS_FILE_ID = 'YOUR_SHEET_DATA_FILE_ID'

# authorization constants
CLIENT_ID_FILE = 'credentials.json'
TOKEN_STORE_FILE = 'token.json'
SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)

# application constants
SOURCES = ('text', 'sheets')
SOURCE = 'text' # Choose one of the data SOURCES
COLUMNS = ['to_name', 'to_title', 'to_company', 'to_address']
TEXT_SOURCE_DATA = (
    ('Ms. Lara Brown', 'Googler', 'Google NYC', '111 8th Ave\nNew York, NY  10011-5201'),
    ('Mr. Jeff Erson', 'Googler', 'Google NYC', '76 9th Ave\nNew York, NY  10011-4962'),
)

def get_http_client():
    """Uses project credentials in CLIENT_ID_FILE along with requested OAuth2
        scopes for authorization, and caches API tokens in TOKEN_STORE_FILE.
    """
    store = file.Storage(TOKEN_STORE_FILE)
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_ID_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())

# service endpoints to Google APIs
HTTP = get_http_client()
DRIVE = discovery.build('drive', 'v3', http=HTTP)
DOCS = discovery.build('docs', 'v1', http=HTTP)
SHEETS = discovery.build('sheets', 'v4', http=HTTP)

def get_data(source):
    """Gets mail merge data from chosen data source.
    """
    if source not in {'sheets', 'text'}:
        raise ValueError('ERROR: unsupported source %r; choose from %r' % (
            source, SOURCES))
    return SAFE_DISPATCH[source]()

def _get_text_data():
    """(private) Returns plain text data; can alter to read from CSV file.
    """
    return TEXT_SOURCE_DATA

def _get_sheets_data(service=SHEETS):
    """(private) Returns data from Google Sheets source. NOTE: this sample
        code gets all cells in 'Sheet1', the first default Sheet in a
        spreadsheet. Use any desired data range (in standard A1 notation).
        This sample app is coded to return only the 2nd row (the data).
    """
    return service.spreadsheets().values().get(spreadsheetId=SHEETS_FILE_ID,
            range='Sheet1').execute().get('values')[1:] # skip header row

# data source dispatch table [better alternative vs. eval()]
SAFE_DISPATCH = {k: globals().get('_get_%s_data' % k) for k in SOURCES}

def _copy_template(tmpl_id, source, service):
    """(private) Copies letter template document using Drive API then
        returns file ID of (new) copy.
    """
    body = {'name': 'Merged form letter (%s)' % source}
    return service.files().copy(body=body, fileId=tmpl_id,
            fields='id').execute().get('id')

def merge_template(tmpl_id, source, service):
    """Copies template document and merges data into newly-minted copy then
        returns its file ID.
    """
    # copy template and set context data struct for merging template values
    copy_id = _copy_template(tmpl_id, source, service)
    context = merge.iteritems() if hasattr({}, 'iteritems') else merge.items()

    # "search & replace" API requests for mail merge substitutions
    reqs = [{'replaceAllText': {
                'containsText': {
                    'text': '{{%s}}' % key.upper(), # {{VARS}} are uppercase
                    'matchCase': True,
                },
                'replaceText': value,
            }} for key, value in context]

    # send requests to Docs API to do actual merge
    DOCS.documents().batchUpdate(body={'requests': reqs},
            documentId=copy_id, fields='').execute()
    return copy_id


if __name__ == '__main__':
    # fill-in your data to merge into document template variables
    merge = {
        # sender data
        'my_name': 'Ayme A. Coder',
        'my_address': '1600 Amphitheatre Pkwy\n'
                      'Mountain View, CA  94043-1351',
        'my_email': 'http://google.com',
        'my_phone': '+1-650-253-0000',
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        # recipient data (supplied by 'text' or 'sheets' data source)
        'to_name': None,
        'to_title': None,
        'to_company': None,
        'to_address': None,
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        'date': time.strftime('%Y %B %d'),
        # - - - - - - - - - - - - - - - - - - - - - - - - - -
        'body': 'Google, headquartered in Mountain View, unveiled the new '
                'Android phone at the Consumer Electronics Show. CEO Sundar '
                'Pichai said in his keynote that users love their new phones.'
    }

    # get row data, then loop through & process each form letter
    data = get_data(SOURCE) # get data from data source
    for i, row in enumerate(data):
        merge.update(dict(zip(COLUMNS, row)))
        print('Merged letter %d: docs.google.com/document/d/%s/edit' % (
                i+1, merge_template(DOCS_FILE_ID, SOURCE, DRIVE)))
# [END mail_merge_python]
