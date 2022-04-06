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

# [START slides_create_bulleted_text]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_bulleted_text(presentation_id, shape_id):
    """
        Run create_bulleted_text the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.\n"
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:

        slides_service = build('slides', 'v1', credentials=creds)
        # Add arrow-diamond-disc bullets to all text in the shape.
        requests = [
            {
                'createParagraphBullets': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'ALL'
                    },
                    'bulletPreset': 'BULLET_ARROW_DIAMOND_DISC'
                }
            }
        ]

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Added bullets to text in shape with ID: {shape_id}")

        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error


if __name__ == '__main__':
    # Put the presentation_id and shape_id
    # to be submitted.
    create_bulleted_text("1VD1xmi1-9DonI4zmCKENTzlVxIL5SdGGTmbHmnBjQ1E", "MyTextBox_9")

# [END slides_create_bulleted_text]
