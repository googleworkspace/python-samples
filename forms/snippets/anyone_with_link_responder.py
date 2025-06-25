# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.file"]
CLIENT_SECRET_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"

# TODO: Replace with your Form ID and responder's email
YOUR_FORM_ID = "YOUR_FORM_ID"


def get_credentials():
  """Gets the credentials for the user."""
  creds = None
  if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          CLIENT_SECRET_FILE, SCOPES
      )
      creds = flow.run_local_server(port=8080)
    with open(TOKEN_FILE, "w") as token:
      token.write(creds.to_json())
  return creds


# [START forms_is_anyone_with_link_responder]
def is_anyone_with_link_responder():
  """Checks if anyone with the link is a responder for the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)
  anyone_with_link_responder = False

  try:
    permissions_result = (
        drive_service.permissions()
        .list(
            fileId=YOUR_FORM_ID,
            fields="permissions(id,type,role,view)",
            includePermissionsForView="published",
        )
        .execute()
    )

    permissions = permissions_result.get("permissions", [])
    if not permissions:
      print(f"No permissions found for form ID: {YOUR_FORM_ID}")
    else:
      for permission in permissions:
        if (
            permission.get("type") == "anyone"
            and permission.get("view") == "published"
            and permission.get("role") == "reader"
        ):
          anyone_with_link_responder = True
          break

    if anyone_with_link_responder:
      print(
          f"Form '{YOUR_FORM_ID}' IS configured for 'Anyone with the link' to"
          " respond."
      )
    else:
      print(
          f"Form '{YOUR_FORM_ID}' is NOT configured for 'Anyone with the link'"
          " to respond."
      )

  except Exception as e:
    print(f"An error occurred: {e}")
  return anyone_with_link_responder


# [END forms_is_anyone_with_link_responder]


# [START forms_set_anyone_with_link_responder]
def set_anyone_with_link_responder():
  """Sets anyone with the link to be a responder for the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)

  permission_body = {
      "type": "anyone",
      "view": "published",  # Key for making it a responder setting
      "role": "reader",
  }

  try:
    response = (
        drive_service.permissions()
        .create(
            fileId=YOUR_FORM_ID,
            body=permission_body,
        )
        .execute()
    )
    print(
        "'Anyone with the link can respond' permission set for form"
        f" {YOUR_FORM_ID}: {response}"
    )
    return True
  except Exception as e:
    print(f"An error occurred: {e}")
  return False


# [END forms_set_anyone_with_link_responder]


# [START forms_remove_anyone_with_link_responder]
def remove_anyone_with_link_responder():
  """Removes anyone with the link as a responder for the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)

  permission_id_to_delete = None

  try:
    permissions_result = (
        drive_service.permissions()
        .list(
            fileId=YOUR_FORM_ID,
            fields="permissions(id,type,role,view)",
            includePermissionsForView="published",
        )
        .execute()
    )

    permissions = permissions_result.get("permissions", [])
    for permission in permissions:
      if (
          permission.get("type") == "anyone"
          and permission.get("role") == "reader"
          and permission.get("view") == "published"
      ):
        permission_id_to_delete = permission.get("id")
        break

    if permission_id_to_delete:
      drive_service.permissions().delete(
          fileId=YOUR_FORM_ID, permissionId=permission_id_to_delete
      ).execute()
      print(
          "Successfully removed 'Anyone with the link' permission (ID:"
          f" {permission_id_to_delete}) from form {YOUR_FORM_ID}."
      )
      return True
    else:
      print(
          "'Anyone with the link can respond' permission not found for form"
          f" {YOUR_FORM_ID}."
      )

  except Exception as e:
    print(f"An error occurred: {e}")
  return False


# [END forms_remove_anyone_with_link_responder]

if __name__ == "__main__":
  is_anyone_with_link_responder()
