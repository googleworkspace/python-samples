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

# [START slides_create_textbox_with_text]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_textbox_with_text(presentation_id, page_id):
    """
    Creates the textbox with text, the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Create a new square textbox, using the supplied element ID.
        element_id = 'MyTextBox_10'
        pt350 = {
            'magnitude': 350,
            'unit': 'PT'
        }
        requests = [
            {
                'createShape': {
                    'objectId': element_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': pt350,
                            'width': pt350
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            },

            # Insert text into the box, using the supplied element ID.
            {
                'insertText': {
                    'objectId': element_id,
                    'insertionIndex': 0,
                    'text': 'New Box Text Inserted!'
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_shape_response = response.get('replies')[0].get('createShape')
        print(f"Created textbox with ID:"
              f"{(create_shape_response.get('objectId'))}")
    except HttpError as error:
        print(f'An error occurred: {error}')

        return error

    return response


if __name__ == '__main__':
    # Put the presentation_id, Page_id of slides whose list needs
    # to be submitted.
    create_textbox_with_text("12SQU9Ik-ShXecJoMtT-LlNwEPiFR7AadnxV2KiBXCnE",
                             "Myfirstpage")

# [END slides_create_textbox_with_text]
