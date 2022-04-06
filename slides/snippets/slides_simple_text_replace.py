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

# [START slides_simple_text_replace]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def simple_text_replace(presentation_id, shape_id, replacement_text):
    """
    Run simple_text_replace the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        slides_service = build('slides', 'v1', credentials=creds)
        # Remove existing text in the shape, then insert new text.
        requests = []
        requests.append({
            'deleteText': {
                'objectId': shape_id,
                'textRange': {
                    'type': 'ALL'
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': shape_id,
                'insertionIndex': 0,
                'text': replacement_text
            }
        })

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print(f"Replaced text in shape with ID: {shape_id}")
        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Text is not merged")
        return error


if __name__ == '__main__':
    # Put the presentation_id, shape_id and replacement_text
    simple_text_replace('10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4',
                        'MyTextBox_6',
                        'GWSpace_now')
