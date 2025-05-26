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

# [START forms_get_responders]

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly"]
CLIENT_SECRET_FILE = "client_secrets.json"
TOKEN_FILE = "token.json"

# TODO: Replace with your Form ID
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


def get_responders():
  """Gets the responders for the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)

  try:
    response = (
        drive_service.permissions()
        .list(
            fileId=YOUR_FORM_ID,
            fields="permissions(id,emailAddress,type,role,view)",
            includePermissionsForView="published",
        )
        .execute()
    )

    published_readers = []
    for permission in response.get("permissions", []):
      # 'view': 'published' indicates it's related to the published link.
      # 'role': 'reader' is standard for responders.
      # 'type': 'user' for specific users, 'anyone' for public.
      if (
          permission.get("view") == "published"
          and permission.get("role") == "reader"
      ):
        published_readers.append(permission)

    if published_readers:
      print("Responders for this form:")
      print(published_readers)
    else:
      print("No specific published readers found for this form.")

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  get_responders()
# [end forms_get_responders]
