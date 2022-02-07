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
# [START gmail_insert_smime_info]

from __future__ import print_function

import create_smime_info
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def insert_smime_info():
    """Upload an S/MIME certificate for the user.
    Print the inserted certificate's id
    Returns : Result object with inserted certificate id and other meta-data

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        user_id = 'gduser1@workspacesamples.dev'
        smime_info = create_smime_info.create_smime_info(cert_filename='xyz', cert_password='xyz')
        send_as_email = None

        if not send_as_email:
            send_as_email = user_id

        # pylint: disable=maybe-no-member
        results = service.users().settings().sendAs().smimeInfo().\
            insert(userId=user_id, sendAsEmail=send_as_email, body=smime_info)\
            .execute()
        print(F'Inserted certificate; id: {results["id"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        results = None

    return results


if __name__ == '__main__':
    insert_smime_info()
# [END gmail_insert_smime_info]
