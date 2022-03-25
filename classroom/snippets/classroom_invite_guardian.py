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
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# [START classroom_invite_guardian]


def classroom_invite_guardian():
    """
    Creates the courses the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n"
    """

    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    guardian_invitation = {
        'invitedEmailAddress': 'guardian@gmail.com',
    }

    try:
        service = build('classroom', 'v1', credentials=creds)
        while True:
            guardian_invitations = service.userProfiles().guardianInvitations()
            guardian_invitation = guardian_invitations.create(
                # You can use a user ID or an email address.
                studentId='student@mydomain.edu',
                body=guardian_invitation).execute()
            print("Invitation created with id: {%s}"
                  % guardian_invitation.get('invitationId'))

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    # Put the course_id, coursework_id and user_id of course whose list needs
    # to be submitted.
    classroom_invite_guardian()
# [END classroom_invite_guardian]
