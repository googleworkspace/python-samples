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

# [START sheets_quickstart]
from __future__ import print_function
import pickle
from sys import exit as sysexit
from os.path import exists
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
SAMPLE_RANGE_NAME = 'Class Data!A2:E'

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    updated_creds = False

    # Check to see if the program can obtain credentials for authorizing api,
    # either from previous token.pickle or from credentials.json
    if not (exists('token.pickle') or exists('credentials.json')):
        print('\nPrerequisite - \'credentials.json\' - file not found. Before'
        ' running again, please follow the Quickstart to'
        ' download the \'credentials.json\' file here: \n\n'
        'https://developers.google.com/sheets/api/quickstart/'
        'python#step_1_turn_on_the\n')
        sysexit()

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time. First, try to read the token.pickle from prior login attempt.
    elif exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If no token.pickle, try to create creds from the credentials.json file
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json', SCOPES)
        creds = flow.run_local_server()
        updated_creds = True

    # If the credentials are not valid, let the user log in.
    if not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            updated_creds = True

    # If updated the credentials, save for next run
    if updated_creds:
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('\n%s, %s' % (row[0], row[4]))

if __name__ == '__main__':
    main()
# [END sheets_quickstart]
