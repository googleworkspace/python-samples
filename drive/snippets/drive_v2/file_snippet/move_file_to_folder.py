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

# [START drive_move_file_to_folder]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def move_file_to_folder(file_id, folder_id):
  """Move specified file to the specified folder.
  Args:
      file_id: Id of the file to move.
      folder_id: Id of the folder
  Print: An object containing the new parent folder and other meta data
  Returns : Parent Ids for the file

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()

  try:
    # call drive api client
    service = build("drive", "v2", credentials=creds)

    # Retrieve the existing parents to remove
    # pylint: disable=maybe-no-member
    file = service.files().get(fileId=file_id, fields="parents").execute()
    previous_parents = ",".join(
        [parent["id"] for parent in file.get("parents")]
    )
    # Move the file to the new folder
    file = (
        service.files()
        .update(
            fileId=file_id,
            addParents=folder_id,
            removeParents=previous_parents,
            fields="id, parents",
        )
        .execute()
    )
    new_parent_folder_id = [parent["id"] for parent in file.get("parents")]
    print(
        f'file with ID : {file.get("id")} moved to folder : '
        f"{new_parent_folder_id}"
    )
    return [parent["id"] for parent in file.get("parents")]

  except HttpError as error:
    print(f"An error occurred: {error}")
    return None


if __name__ == "__main__":
  move_file_to_folder(
      file_id="14fesChjgzDA7lUu9ZeGqXOuXMPgaVkxS",
      folder_id="1KzT9gjq-AHfciwNzKjh7nUd6prrQOA4",
  )
# [END drive_move_file_to_folder]
