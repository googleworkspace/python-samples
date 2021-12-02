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

# pylint: disable=E1102
# python3
"""Functionality for creating and writing to a spreadsheet."""


def CreateSpreadsheet(sheets_service, title, sheet_titles):
    """Creates an empty spreadsheet.

    It creates a spreadsheet with the provided title, and creates a sheet for
    each entry in the sheet_titles list with the corresponding sheet title.
    """
    sheets = []
    for sheet_title in sheet_titles:
        sheet = {
            'properties': {
                'title': sheet_title,
            },
        }
        sheets.append(sheet)

    spreadsheet = {
        'properties': {
            'title': title,
        },
        'sheets': sheets,
    }
    return sheets_service.spreadsheets().create(body=spreadsheet).execute()


class SpreadsheetWriter(object):
    """Queues writes for modifying a spreadsheet.

    Call ExecuteBatchUpdate to flush pending writes.
    """

    def __init__(self, sheets_service, spreadsheet_id):
        self._sheets_service = sheets_service
        self._spreadsheet_id = spreadsheet_id
        self._requests = []

    def InsertColumn(self, sheet_id, column_index):
        request = {
            'insertDimension': {
                'range': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': column_index,
                    'endIndex': column_index + 1,
                },
            }
        }
        self._requests.append(request)

    def PopulateColumn(self, sheet_id, column_index, column_id, values):
        # Include the column ID in the column values
        values = [column_id] + values

        # Populate the column with the values
        rows = []
        for value in values:
            row_data = {
                'values': [
                    {
                        'userEnteredValue': {
                            'stringValue': value
                        }
                    }
                ]
            }
            rows.append(row_data)

        update_request = {
            'updateCells': {
                'rows': rows,
                'fields': 'userEnteredValue',
                'start': {
                    'sheetId': sheet_id,
                    'rowIndex': 0,
                    'columnIndex': column_index
                }
            }
        }
        self._requests.append(update_request)

        # Add developer metadata to the column to make it easier to read later
        # by being able to just query it by the column ID
        metadata_request = {
            'createDeveloperMetadata': {
                'developerMetadata': {
                    'metadataKey': 'column_id',
                    'metadataValue': column_id,
                    'location': {
                        'dimensionRange': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS',
                            'startIndex': column_index,
                            'endIndex': column_index + 1,
                        }
                    },
                    'visibility': 'DOCUMENT',
                }
            }
        }
        self._requests.append(metadata_request)

    def AddTemplateIdToSpreadsheetMetadata(self, template_id):
        request = {
            'createDeveloperMetadata': {
                'developerMetadata': {
                    'metadataKey': 'template_id',
                    'metadataValue': template_id,
                    'location': {
                        'spreadsheet': True
                    },
                    'visibility': 'DOCUMENT',
                }
            }
        }
        self._requests.append(request)

    def ExecuteBatchUpdate(self):
        body = {'requests': self._requests}
        self._requests = []
        return self._sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=self._spreadsheet_id, body=body).execute()
