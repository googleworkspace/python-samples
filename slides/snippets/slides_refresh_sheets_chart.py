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

# [START slides_refresh_sheets_chart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def refresh_sheets_chart(presentation_id, presentation_chart_id):
    """
        refresh_sheets_chart the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        slides_service = build('slides', 'v1', credentials=creds)
        # Refresh an existing linked Sheets chart embedded in a presentation.
        requests = [
            {
                'refreshSheetsChart': {
                    'objectId': presentation_chart_id
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Refreshed a linked Sheets chart with ID:{presentation_chart_id}")
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the presentation_id, presentation_chart_id
    # to be submitted.
    refresh_sheets_chart("10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4", "1107320627")
    # [END slides_refresh_sheets_chart]
