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

# [START sheets_get_values]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def append_values(spreadsheet_id, range_name, value_input_option,
                  _values):
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
        print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
        return result

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    append_values("1CM29gwKIzeXsAppeNwrc8lbYaVMmUclprLuLYuHog4k",
                  "A1:C2", "USER_ENTERED",
                  [
                      ['F', 'B'],
                      ['C', 'D']
                  ])
    # [END sheets_append_values]
