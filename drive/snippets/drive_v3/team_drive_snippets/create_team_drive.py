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

# [START drive_create_team_drive]
import uuid

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_team_drive():
  """Create a drive for team.
  Returns: ID of the created drive

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()

  try:
    # call drive api client
    service = build("drive", "v3", credentials=creds)

    # pylint: disable=maybe-no-member
    team_drive_metadata = {"name": "Project Resources"}
    request_id = str(uuid.uuid4())
    team_drive = (
        service.teamdrives()
        .create(body=team_drive_metadata, requestId=request_id, fields="id")
        .execute()
    )
    print(f'Team Drive ID: {team_drive.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    team_drive = None

  return team_drive.get("id")


if __name__ == "__main__":
  create_team_drive()
# [END drive_create_team_drive]
