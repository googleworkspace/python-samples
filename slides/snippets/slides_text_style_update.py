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

# [START slides_text_style_update]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def text_style_update(presentation_id, shape_id):
    """
    create_sheets_chart the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Update the text style so that the first 5 characters are bolded
        # and italicized, the next 5 are displayed in blue 14 pt Times
        # New Roman font, and the next 5 are hyperlinked.
        requests = [
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 0,
                        'endIndex': 5
                    },
                    'style': {
                        'bold': True,
                        'italic': True
                    },
                    'fields': 'bold,italic'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 5,
                        'endIndex': 10
                    },
                    'style': {
                        'fontFamily': 'Times New Roman',
                        'fontSize': {
                            'magnitude': 14,
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': 1.0,
                                    'green': 0.0,
                                    'red': 0.0
                                }
                            }
                        }
                    },
                    'fields': 'foregroundColor,fontFamily,fontSize'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 10,
                        'endIndex': 15
                    },
                    'style': {
                        'link': {
                            'url': 'www.example.com'
                        }
                    },
                    'fields': 'link'
                }
            }
        ]

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Updated the text style for shape with ID:{shape_id}")

        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the presentation_id, shape_id of slides
    # to be submitted.
    text_style_update("10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4",
                      "MyTextBox_9")
# [END slides_text_style_update]
