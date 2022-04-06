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

# [START slides_create_presentation]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_presentation(title):
    """
        Creates the Presentation the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.\n"
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)

        body = {
            'title': title
        }
        presentation = service.presentations() \
            .create(body=body).execute()
        print(f"Created presentation with ID:"
              f"{(presentation.get('presentationId'))}")
        return presentation

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("presentation not created")
        return error


if __name__ == '__main__':
    # Put the title of the presentation

    create_presentation("finalp")

# [END slides_create_presentation]
