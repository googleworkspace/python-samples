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

# [START drive_recover_drives]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def recover_drives(real_user):
  """Find all shared drives without an organizer and add one.
  Args:
      real_user:User ID for the new organizer.
  Returns:
      drives object

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()
  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    drives = []

    # pylint: disable=maybe-no-member
    page_token = None
    new_organizer_permission = {
        "type": "user",
        "role": "organizer",
        "emailAddress": "user@example.com",
    }
    new_organizer_permission["emailAddress"] = real_user

    while True:
      response = (
          service.drives()
          .list(
              q="organizerCount = 0",
              fields="nextPageToken, drives(id, name)",
              useDomainAdminAccess=True,
              pageToken=page_token,
          )
          .execute()
      )
      for drive in response.get("drives", []):
        print(
            "Found shared drive without organizer: "
            f"{drive.get('title')}, {drive.get('id')}"
        )
        permission = (
            service.permissions()
            .create(
                fileId=drive.get("id"),
                body=new_organizer_permission,
                useDomainAdminAccess=True,
                supportsAllDrives=True,
                fields="id",
            )
            .execute()
        )
        print(f'Added organizer permission: {permission.get("id")}')

      drives.extend(response.get("drives", []))
      page_token = response.get("nextPageToken", None)
      if page_token is None:
        break

  except HttpError as error:
    print(f"An error occurred: {error}")

  return drives


if __name__ == "__main__":
  recover_drives(real_user="gduser1@workspacesamples.dev")
# [END drive_recover_drives]
