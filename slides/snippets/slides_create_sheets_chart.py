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

# [START slides_create_sheets_chart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_sheets_chart(presentation_id, page_id, spreadsheet_id,
                        sheet_chart_id):
    """
    create_sheets_chart the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        slides_service = build('slides', 'v1', credentials=creds)
        # Embed a Sheets chart (indicated by the spreadsheet_id and
        # sheet_chart_id) onto a page in the presentation.
        # Setting the linking mode as "LINKED" allows the
        # chart to be refreshed if the Sheets version is updated.

        emu4m = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }

        presentation_chart_id = 'MyEmbeddedChart'
        requests = [
            {
                'createSheetsChart': {
                    'objectId': presentation_chart_id,
                    'spreadsheetId': spreadsheet_id,
                    'chartId': sheet_chart_id,
                    'linkingMode': 'LINKED',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': emu4m,
                            'width': emu4m
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 100000,
                            'translateY': 100000,
                            'unit': 'EMU'
                        }
                    }
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Added a linked Sheets chart with ID: {presentation_chart_id}")
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the presentation_id, Page_id of slides
    # spreadsheet_id and sheet_chart_id to be submitted.
    create_sheets_chart("10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4",
                        "FIRSTSLIDE",
                        "17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM",
                        "1107320627")
