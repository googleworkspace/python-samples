"""Copyright 2022 Google LLC

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

# [START drive_recover_team_drives]

from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def recover_team_drives(real_user):
    """Finds all Team Drives without an organizer and add one
    Args:
        real_user:User ID for the new organizer.
    Returns:
        team drives_object.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()

    try:
        # call drive api client
        service = build('drive', 'v3', credentials=creds)

        # pylint: disable=maybe-no-member
        team_drives = []

        page_token = None
        new_organizer_permission = {'type': 'user',
                                    'role': 'organizer',
                                    'value': 'user@example.com'}

        new_organizer_permission['emailAddress'] = real_user

        while True:
            response = service.teamdrives().list(q='organizerCount = 0',
                                                 fields='nextPageToken, '
                                                        'teamDrives(id, '
                                                        'name)',
                                                 useDomainAdminAccess=True,
                                                 pageToken=page_token
                                                 ).execute()

            for team_drive in response.get('teamDrives', []):
                print('Found Team Drive without organizer: {team_drive.get('
                      '"title")},{team_drive.get("id")}')
                permission = service.permissions().create(
                    fileId=team_drive.get('id'),
                    body=new_organizer_permission, useDomainAdminAccess=True,
                    supportsTeamDrives=True, fields='id').execute()
                print(F'Added organizer permission:{permission.get("id")}')

            team_drives.extend(response.get('teamDrives', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        team_drives = None

    print(team_drives)


if __name__ == '__main__':
    recover_team_drives(real_user='gduser1@workspacesamples.dev')
# [END drive_recover_team_drives]
