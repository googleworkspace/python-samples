"""
Copyright 2018 Google LLC

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

# [START slides_quickstart]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/presentations.readonly']

# The ID of a sample presentation.
PRESENTATION_ID = '1EAYk18WDjIG-zp_0vLm3CsfQh_i8eXc67Jo2O9C6Vuc'


def main():
    """Shows basic usage of the Slides API.
    Prints the number of slides and elements in a sample presentation.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """
    creds, _ = google.auth.default()

    try:
        service = build('slides', 'v1', credentials=creds)

        # Call the Slides API
        # pylint: disable=no-member
        presentation = service.presentations().get(
            presentationId=PRESENTATION_ID).execute()
        slides = presentation.get('slides')

        print('The presentation contains {} slides:'.format(len(slides)))
        for i, slide in enumerate(slides):
            print('- Slide #{} contains {} elements.'.format(
                i + 1, len(slide.get('pageElements'))))
    except HttpError as err:
        print(err)


if __name__ == '__main__':
    main()
# [END slides_quickstart]
