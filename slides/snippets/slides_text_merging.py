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

# [START slides_text_merging]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def text_merging(template_presentation_id, data_spreadsheet_id):
    """
    Run Text merging the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    responses = []

    try:

        service = build('slides', 'v1', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        # Use the Sheets API to load data, one record per row.
        data_range_notation = 'Customers!A2:M6'
        sheets_response = sheets_service.spreadsheets().values().get(
            spreadsheetId=data_spreadsheet_id,
            range=data_range_notation).execute()
        values = sheets_response.get('values')

        # For each record, create a new merged presentation.
        for row in values:
            customer_name = row[2]  # name in column 3
            case_description = row[5]  # case description in column 6
            total_portfolio = row[11]  # total portfolio in column 12

            # Duplicate the template presentation using the Drive API.
            copy_title = customer_name + ' presentation'
            body = {
                'name': copy_title
            }
            drive_response = drive_service.files().copy(
                fileId=template_presentation_id, body=body).execute()
            presentation_copy_id = drive_response.get('id')

            # Create the text merge (replaceAllText) requests
            # for this presentation.
            requests = [
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{customer-name}}',
                            'matchCase': True
                        },
                        'replaceText': customer_name
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{case-description}}',
                            'matchCase': True
                        },
                        'replaceText': case_description
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{total-portfolio}}',
                            'matchCase': True
                        },
                        'replaceText': total_portfolio
                    }
                }
            ]

            # Execute the requests for this presentation.
            body = {
                'requests': requests
            }
            response = service.presentations().batchUpdate(
                presentationId=presentation_copy_id, body=body).execute()
            # [START_EXCLUDE silent]
            responses.append(response)
            # [END_EXCLUDE]
            # Count the total number of replacements made.
            num_replacements = 0
            for reply in response.get('replies'):
                if reply.get('occurrencesChanged') is not None:
                    num_replacements += reply.get('replaceAllText') \
                        .get('occurrencesChanged')
            print(f"Created presentation for "
                  f"{customer_name} with ID: {presentation_copy_id}")
            print(f"Replaced {num_replacements} text instances")

        return response

    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the template_presentation_id, data_spreadsheet_id
    # of slides

    text_merging("10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4",
                 "17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM")
    # [END slides_text_merging]
