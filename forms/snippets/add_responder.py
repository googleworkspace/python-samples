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

# [START forms_add_responder]

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


def add_responder():
  """Adds the responder to the form."""
  creds = get_credentials()
  drive_service = build("drive", "v3", credentials=creds)

  permission_body = {
      "view": "published",
      "role": "reader",
      "type": "user",
      "emailAddress": YOUR_RESPONDER_EMAIL,
  }

  try:
    response = (
        drive_service.permissions()
        .create(
            fileId=YOUR_FORM_ID,
            body=permission_body,
            sendNotificationEmail=False,  # Optional: to avoid sending an email
        )
        .execute()
    )
    print(
        f"Added responder {YOUR_RESPONDER_EMAIL}. Permission ID:"
        f" {response.get('id')}"
    )
    print(response)
  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  add_responder()
# [end forms_add_responder]
