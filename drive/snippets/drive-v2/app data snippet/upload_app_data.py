"""Copyright 2018 Google LLC

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

# [START drive_upload_app_data]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_app_data():
    """Insert a file in the application data folder and prints file Id.
    Returns : ID's of the inserted files

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # call drive api client
        service = build('drive', 'v2', credentials=creds)

        file_metadata = {
            'title': 'abc.txt',
            'parents': [{
                'id': 'appDataFolder'
            }]
        }
        media = MediaFileUpload('abc.txt',
                                mimetype='text/txt',
                                resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().insert(body=file_metadata, media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('id')


if __name__ == '__main__':
    upload_app_data()
# [END drive_upload_app_data]
