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
# [START drive_upload_with_conversion]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_with_conversion():
    """Upload file with conversion
    Returns: ID of the file uploaded

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v2', credentials=creds)

        file_metadata = {
            'title': 'My Report',
            'mimeType': 'application/vnd.google-apps.spreadsheet'
        }
        media = MediaFileUpload('report.csv', mimetype='text/csv',
                                resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().insert(body=file_metadata,
                                      media_body=media, fields='id').execute()
        print(F'File with ID: "{file.get("id")}" has been uploaded.')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_with_conversion()
# [END drive_upload_with_conversion]
