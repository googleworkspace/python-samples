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

# [START forms_remove_responder]

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
YOUR_RESPONDER_EMAIL = "user@example.com"


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


def remove_responder():
  """Removes the responder for the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)

  try:
    # First, find the permission ID for the user
    permissions_result = (
        drive_service.permissions()
        .list(
            fileId=YOUR_FORM_ID,
            fields="permissions(id,emailAddress,role,view,type)",
            includePermissionsForView="published",
        )
        .execute()
    )

    permission_id_to_delete = None
    for p in permissions_result.get("permissions", []):
      if (
          p.get("emailAddress") == YOUR_RESPONDER_EMAIL
          and p.get("role") == "reader"
          and p.get("view") == "published"
          and p.get("type") == "user"
      ):
        permission_id_to_delete = p.get("id")
        break

    if permission_id_to_delete:
      drive_service.permissions().delete(
          fileId=YOUR_FORM_ID, permissionId=permission_id_to_delete
      ).execute()
      print(
          f"Successfully removed responder {YOUR_RESPONDER_EMAIL} (Permission"
          f" ID: {permission_id_to_delete}) from form {YOUR_FORM_ID}."
      )
    else:
      print(
          f"Responder {YOUR_RESPONDER_EMAIL} not found or not a published"
          f" reader for form {YOUR_FORM_ID}."
      )

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  remove_responder()
# [END forms_remove_responder]
