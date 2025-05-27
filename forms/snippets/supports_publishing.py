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

# [START forms_supports_publishing]

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# If modifying these SCOPES, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/forms.body"]
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"
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


def supports_publishing():
  """Checks if the form supports publishing."""
  creds = get_credentials()
  form_service = build(
      "forms",
      "v1",
      credentials=creds,
      discoveryServiceUrl=DISCOVERY_DOC,
      static_discovery=False,
  )

  is_legacy = True  # Assume legacy until proven otherwise
  try:
    form_metadata = form_service.forms().get(formId=YOUR_FORM_ID).execute()
    # If 'publishSettings' field exists, it's not a legacy form regarding this feature.
    if "publishSettings" in form_metadata:
      print(
          f"Form '{YOUR_FORM_ID}' (Title:"
          f" {form_metadata.get('info', {}).get('title')}) is NOT a legacy form"
          " (supports publishSettings)."
      )
      is_legacy = False
    else:
      print(
          f"Form '{YOUR_FORM_ID}' (Title:"
          f" {form_metadata.get('info', {}).get('title')}) IS a legacy form"
          " (does not have publishSettings field)."
      )
    return not is_legacy  # Returns true if it supports publishing

  except Exception as e:
    print(f"An error occurred while checking form {YOUR_FORM_ID}: {e}")
    # Depending on the error, it might indicate non-existence or access issues,
    # not necessarily legacy status.
    return None


if __name__ == "__main__":
  supports_publishing()
# [end forms_supports_publishing]
