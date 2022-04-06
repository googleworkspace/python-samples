"""
Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# [START sheets_conditional_formatting]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def conditional_formatting(spreadsheet_id):
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('sheets', 'v4', credentials=creds)

        my_range = {
            'sheetId': 0,
            'startRowIndex': 1,
            'endRowIndex': 11,
            'startColumnIndex': 0,
            'endColumnIndex': 4,
        }
        requests = [{
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [my_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=GT($D2,median($D$2:$D$11))'
                            }]
                        },
                        'format': {
                            'textFormat': {
                                'foregroundColor': {'red': 0.8}
                            }
                        }
                    }
                },
                'index': 0
            }
        }, {
            'addConditionalFormatRule': {
                'rule': {
                    'ranges': [my_range],
                    'booleanRule': {
                        'condition': {
                            'type': 'CUSTOM_FORMULA',
                            'values': [{
                                'userEnteredValue':
                                    '=LT($D2,median($D$2:$D$11))'
                            }]
                        },
                        'format': {
                            'backgroundColor': {
                                'red': 1,
                                'green': 0.4,
                                'blue': 0.4
                            }
                        }
                    }
                },
                'index': 0
            }
        }]
        body = {
            'requests': requests
        }
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(f"{(len(response.get('replies')))} cells updated.")
        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id
    conditional_formatting("1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k")
    # [END sheets_conditional_formatting]
