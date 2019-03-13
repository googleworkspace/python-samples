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
docs-mail-merge.py (2.x or 3.x)

Google Docs (REST) API mail-merge sample app
"""
from __future__ import print_function
import time

from googleapiclient import discovery
from httplib2 import Http
from oauth2client import file, client, tools

# fill-in your template file ID
DOCS_FILE_ID = 'YOUR_TMPL_DOC_FILE_ID'      # Docs template
SHEETS_FILE_ID = 'YOUR_SHEET_DATA_FILE_ID'  # Sheets data source
CREDS_FILE = 'credentials.json'
SCOPES = (  # iterable or space-delimited string
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets.readonly',
)
COLUMNS = ['to_name', 'to_title', 'to_company', 'to_address']
OUTPUT = True # change to False to suppress output
SOURCES = ('text', 'sheets')
SOURCE = 'text' # or 'sheets' to change data source

def get_http_client():
    """Manage OAuth tokens in 'token.json' file given the downloaded
       'credentials.json' file along with requested OAuth2 scopes.
    """
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(CREDS_FILE, SCOPES)
        creds = tools.run_flow(flow, store)
    return creds.authorize(Http())

# create service endpoints to the 3 APIs
HTTP = get_http_client()
DRIVE = discovery.build('drive', 'v3', http=HTTP)
DOCS = discovery.build('docs', 'v1', http=HTTP)
SHEETS = discovery.build('sheets', 'v4', http=HTTP)

# plain text data source
TARGET_TEXT = [
    'Ms. Lara Brown', 'Googler', 'Google NYC',
    '111 8th Ave\nNew York, NY  10011-5201'
]

# fill-in your data to merge into document template variables
merge = {
    'my_name': 'Mr. Jeff Erson',
    'my_address': '76 9th Ave\nNew York, NY  10011-4962',
    'my_email': 'http://google.com',
    'my_phone': '+1-212-565-0000',
    # - - - - - - - - - - - - - - - - - - - - - - - - - -
    'date': time.ctime(),
    # - - - - - - - - - - - - - - - - - - - - - - - - - -
    'body': 'Google, headquartered in Mountain View, unveiled the new Android '
            'phone at the Consumer Electronics Show. CEO Sundar Pichai said '
            'in his keynote that users love their new Android phones.'
}

def get_data(source='text', output=True):
    """Gets mail merge data from chosen data source.
    """
    if source not in {'sheets', 'text'}:
        raise ValueError('ERROR: unsupported source %r; choose %r' % (
            source, SOURCES))
    func = SAFE_DISPATCH[source]
    return dict(zip(COLUMNS, func(output=output)))

def _get_text_data(output=False):
    """Private function that returns data from plain text source.
    """
    if output:
        print(' - Using static text data')
    return TARGET_TEXT

def _get_sheets_data(service=SHEETS, output=False):
    """Private function that returns data from Google Sheets source.
        Note: this sample code gets all cells in 'Sheet1', the first
        default Sheet in a spreadsheet. Use any desired data range
        you need (in standard A1 notation). Sample returns only 1 row.
        The 'output' flag toggles verbose output.
    """
    if output:
        print(' - Using data from Google Sheets')
    return service.spreadsheets().values().get(spreadsheetId=SHEETS_FILE_ID,
            range='Sheet1').execute().get('values')[0] # one row only

SAFE_DISPATCH = {k: globals().get('_get_%s_data' % k) for k in SOURCES}

def _copy_template(tmpl_id, source, service=DRIVE, output=False):
    """Private function that copies the letter template document then
       returns the new file ID. The 'output' flag toggles verbose output.
    """
    body = {'name': 'Merged form letter (%s)' % source}
    if output:
        print(' - Copying template document as %r' % body['name'])

    # Call the Drive API to copy the template document.
    return service.files().copy(body=body, fileId=tmpl_id,
            fields='id').execute().get('id')

def merge_template(tmpl_id=DOCS_FILE_ID, source='text', output=False):
    """Merge the new letter template copy and return its file ID.
       The 'output' flag toggles verbose output.
    """
    # Copy the template and get the file ID of the new copy.
    copy_id = _copy_template(tmpl_id, source, DRIVE, output)

    # Build the requests to make all substitutions in the mail merge.
    if output:
        print(' - Replacing placeholder variables')

    # Get key-value pairs (prefer iterators) and merge template values
    context = merge.iteritems() if hasattr({}, 'iteritems') else merge.items()
    reqs = [{'replaceAllText': {
                'containsText': {
                    'text': '{{%s}}' % key.upper(),
                    'matchCase': True,
                },
                'replaceText': value,
            }} for key, value in context]

    # Use the Docs API to merge the data in the new copied document.
    DOCS.documents().batchUpdate(body={'requests': reqs},
            documentId=copy_id, fields='').execute()
    return copy_id


if __name__ == '__main__':
    if SOURCE in SOURCES:
        merge.update(get_data(SOURCE, OUTPUT))
        fid = merge_template(source=SOURCE, output=OUTPUT)
        if OUTPUT:
            print(' - Merged letter: docs.google.com/document/d/%s/edit' % fid)
