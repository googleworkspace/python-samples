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

from __future__ import print_function


class SpreadsheetSnippets(object):
    def __init__(self, service):
        self.service = service

    def create(self, title):
        service = self.service
        # [START sheets_create]
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(body=spreadsheet,
                                                    fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))
        # [END sheets_create]
        return spreadsheet.get('spreadsheetId')

    def batch_update(self, spreadsheet_id, title, find, replacement):
        service = self.service
        # [START sheets_batch_update]
        requests = []
        # Change the spreadsheet's title.
        requests.append({
            'updateSpreadsheetProperties': {
                'properties': {
                    'title': title
                },
                'fields': 'title'
            }
        })
        # Find and replace text
        requests.append({
            'findReplace': {
                'find': find,
                'replacement': replacement,
                'allSheets': True
            }
        })
        # Add additional requests (operations) ...

        body = {
            'requests': requests
        }
        response = service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        find_replace_response = response.get('replies')[1].get('findReplace')
        print('{0} replacements made.'.format(
            find_replace_response.get('occurrencesChanged')))
        # [END sheets_batch_update]
        return response

    def get_values(self, spreadsheet_id, range_name):
        service = self.service
        # [START sheets_get_values]
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id, range=range_name).execute()
        rows = result.get('values', [])
        print('{0} rows retrieved.'.format(len(rows)))
        # [END sheets_get_values]
        return result

    def batch_get_values(self, spreadsheet_id, _range_names):
        service = self.service
        # [START sheets_batch_get_values]
        range_names = [
            # Range names ...
        ]
        # [START_EXCLUDE silent]
        range_names = _range_names
        # [END_EXCLUDE]
        result = service.spreadsheets().values().batchGet(
            spreadsheetId=spreadsheet_id, ranges=range_names).execute()
        ranges = result.get('valueRanges', [])
        print('{0} ranges retrieved.'.format(len(ranges)))
        # [END sheets_batch_get_values]
        return result

    def update_values(self, spreadsheet_id, range_name, value_input_option,
                      _values):
        service = self.service
        # [START sheets_update_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
        # [END sheets_update_values]
        return result

    def batch_update_values(self, spreadsheet_id, range_name,
                            value_input_option, _values):
        service = self.service
        # [START sheets_batch_update_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        data = [
            {
                'range': range_name,
                'values': values
            },
            # Additional ranges to update ...
        ]
        body = {
            'valueInputOption': value_input_option,
            'data': data
        }
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id, body=body).execute()
        print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
        # [END sheets_batch_update_values]
        return result

    def append_values(self, spreadsheet_id, range_name, value_input_option,
                      _values):
        service = self.service
        # [START sheets_append_values]
        values = [
            [
                # Cell values ...
            ],
            # Additional rows ...
        ]
        # [START_EXCLUDE silent]
        values = _values
        # [END_EXCLUDE]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells appended.'.format(result
                                           .get('updates')
                                           .get('updatedCells')))
        # [END sheets_append_values]
        return result

    def pivot_tables(self, spreadsheet_id):
        service = self.service
        # Create two sheets for our pivot table.
        body = {
            'requests': [{
                'addSheet': {}
            }, {
                'addSheet': {}
            }]
        }
        batch_update_response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        source_sheet_id = batch_update_response.get('replies')[0] \
            .get('addSheet').get('properties').get('sheetId')
        target_sheet_id = batch_update_response.get('replies')[1] \
            .get('addSheet').get('properties').get('sheetId')
        requests = []
        # [START sheets_pivot_tables]
        requests.append({
            'updateCells': {
                'rows': {
                    'values': [
                        {
                            'pivotTable': {
                                'source': {
                                    'sheetId': source_sheet_id,
                                    'startRowIndex': 0,
                                    'startColumnIndex': 0,
                                    'endRowIndex': 20,
                                    'endColumnIndex': 7
                                },
                                'rows': [
                                    {
                                        'sourceColumnOffset': 1,
                                        'showTotals': True,
                                        'sortOrder': 'ASCENDING',

                                    },

                                ],
                                'columns': [
                                    {
                                        'sourceColumnOffset': 4,
                                        'sortOrder': 'ASCENDING',
                                        'showTotals': True,

                                    }
                                ],
                                'values': [
                                    {
                                        'summarizeFunction': 'COUNTA',
                                        'sourceColumnOffset': 4
                                    }
                                ],
                                'valueLayout': 'HORIZONTAL'
                            }
                        }
                    ]
                },
                'start': {
                    'sheetId': target_sheet_id,
                    'rowIndex': 0,
                    'columnIndex': 0
                },
                'fields': 'pivotTable'
            }
        })
        body = {
            'requests': requests
        }
        response = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        # [END sheets_pivot_tables]
        return response

    def conditional_formatting(self, spreadsheet_id):
        service = self.service

        # [START sheets_conditional_formatting]
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
        print('{0} cells updated.'.format(len(response.get('replies'))))
        # [END sheets_conditional_formatting]
        return response

    def filter_views(self, spreadsheet_id):
        service = self.service

        # [START sheets_filter_views]
        my_range = {
            'sheetId': 0,
            'startRowIndex': 0,
            'startColumnIndex': 0,
        }
        addFilterViewRequest = {
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

        body = {'requests': [addFilterViewRequest]}
        addFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        duplicateFilterViewRequest = {
            'duplicateFilterView': {
                'filterId':
                addFilterViewResponse['replies'][0]['addFilterView']['filter']
                ['filterViewId']
            }
        }

        body = {'requests': [duplicateFilterViewRequest]}
        duplicateFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()

        updateFilterViewRequest = {
            'updateFilterView': {
                'filter': {
                    'filterViewId': duplicateFilterViewResponse['replies'][0]
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

        body = {'requests': [updateFilterViewRequest]}
        updateFilterViewResponse = service.spreadsheets() \
            .batchUpdate(spreadsheetId=spreadsheet_id, body=body).execute()
        print(str(updateFilterViewResponse))
        # [END sheets_filter_views]
