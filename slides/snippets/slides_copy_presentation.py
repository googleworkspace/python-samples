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

# [START slides_copy_presentation]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def copy_presentation(presentation_id, copy_title):
    creds, _ = google.auth.default()
    try:
        drive_service = build('drive', 'v3', credentials=creds)
        body = {
            'name': copy_title
        }
        drive_response = drive_service.files().copy(
            fileId=presentation_id, body=body).execute()
        presentation_copy_id = drive_response.get('id')

    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Slides not created")
        return error

    return presentation_copy_id
    # [END slides_copy_presentation]


if __name__ == '__main__':
    # Put the presentation_id, Page_id of slides whose list needs
    # to be submitted.
    copy_presentation("16eRvJHRrM8Sej5YA0yCHVzQCPLz31-JhbOa4XpP8Yko", "wspace")
