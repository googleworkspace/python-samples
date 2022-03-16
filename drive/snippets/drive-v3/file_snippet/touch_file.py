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
# [START drive_touch_file]

from __future__ import print_function

from datetime import datetime

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def touch_file(real_file_id, real_timestamp):
    """Change the file's modification timestamp.
    Args:
        real_file_id: ID of the file to change modified time
        real_timestamp: Timestamp to override Modified date time of the file
    Returns : Modified Date and time.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('drive', 'v3', credentials=creds)

        file_metadata = {
            'modifiedTime': datetime.utcnow().isoformat() + 'Z'
        }
        # pylint: disable=maybe-no-member
        file_id = real_file_id
        file_metadata['modifiedTime'] = real_timestamp
        file = service.files().update(fileId=file_id, body=file_metadata,
                                      fields='id, modifiedTime').execute()
        print(F'Modified time: {file.get("modifiedTime")}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        file = None

    return file.get('modifiedDate')


if __name__ == '__main__':
    touch_file(real_file_id='17EqlSf7FpPU95SS00sICyVzQHpeET1cz',
               real_timestamp='2022-03-02T05:43:27.504Z')
# [END drive_touch_file]
