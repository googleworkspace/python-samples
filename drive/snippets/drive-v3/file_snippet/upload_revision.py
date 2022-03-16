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
# [START drive_upload_revision]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def upload_revision(real_file_id):
    """Replace the old file with new one on same file ID
    Args: ID of the file to be replaced
    Returns: file ID

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)
        file_id = real_file_id
        media = MediaFileUpload('download.jpeg',
                                mimetype='image/jpeg',
                                resumable=True)
        # pylint: disable=maybe-no-member
        file = service.files().update(fileId=file_id,
                                      body={},
                                      media_body=media,
                                      fields='id').execute()
        print(F'File ID: {file.get("id")}')

    except HttpError as error:
        print(F'An error occurred: {error}')

    return file.get('id')


if __name__ == '__main__':
    upload_revision(real_file_id='1jJTiihczk_xSNPVLwMySQBJACXYdpGTi')
# [END drive_upload_revision]
