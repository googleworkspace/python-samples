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

# [START drive_list_appdata]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def list_appdata():
  """List all files inserted in the application data folder
  prints file titles with Ids.
  Returns : List of items

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()

  try:
    # call drive api client
    service = build("drive", "v2", credentials=creds)

    # pylint: disable=maybe-no-member
    response = (
        service.files()
        .list(
            spaces="appDataFolder",
            fields="nextPageToken, items(id, title)",
            maxResults=10,
        )
        .execute()
    )
    for file in response.get("items", []):
      # Process change
      print(f'Found file: {file.get("title")} ,{file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    response = None

  return response.get("items")


if __name__ == "__main__":
  list_appdata()
# [END drive_list_appdata]
