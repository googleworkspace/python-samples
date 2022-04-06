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

# [START sheets_filter_views]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def filter_views(spreadsheet_id):
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
            'startRowIndex': 0,
            'startColumnIndex': 0,
        }
        addfilterviewrequest = {
            'addFilterView': {
                'filter': {
                    'title': 'Sample Filter',
                    'range': my_range,
                    'sortSpecs': [{
                        'dimensionIndex': 3,
                        'sortOrder': 'DESCENDING'
                    }],
                    'criteria': {
                        0: {
                            'hiddenValues': ['Panel']
                        },
                        6: {
                            'condition': {
                                'type': 'DATE_BEFORE',
                                'values': {
                                    'userEnteredValue': '4/30/2016'
                                }
                            }
                        }
                    }
                }
            }
        }

        body = {'requests': [addfilterviewrequest]}
        addfilterviewresponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        duplicatefilterviewrequest = {
            'duplicateFilterView': {
                'filterId':
                    addfilterviewresponse['replies'][0]
                    ['addFilterView']['filter']
                    ['filterViewId']
            }
        }

        body = {'requests': [duplicatefilterviewrequest]}
        duplicatefilterviewresponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        updatefilterviewrequest = {
            'updateFilterView': {
                'filter': {
                    'filterViewId': duplicatefilterviewresponse['replies'][0]
                    ['duplicateFilterView']['filter']['filterViewId'],
                    'title': 'Updated Filter',
                    'criteria': {
                        0: {},
                        3: {
                            'condition': {
                                'type': 'NUMBER_GREATER',
                                'values': {
                                    'userEnteredValue': '5'
                                }
                            }
                        }
                    }
                },
                'fields': {
                    'paths': ['criteria', 'title']
                }
            }
        }

        body = {'requests': [updatefilterviewrequest]}
        updatefilterviewresponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(str(updatefilterviewresponse))
    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    # Pass: spreadsheet_id
    filter_views("1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k")
    # [END sheets_filter_views]
