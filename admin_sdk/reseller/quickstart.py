# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START admin_sdk_reseller_quickstart]
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/apps.order"]


def main():
  """Calls the Admin SDK Reseller API. Prints the customer ID, SKU ID,
  and plan name of the first 10 subscriptions managed by the domain.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  service = build("reseller", "v1", credentials=creds)

  # Call the Admin SDK Reseller API
  print("Getting the first 10 subscriptions")
  results = service.subscriptions().list(maxResults=10).execute()
  subscriptions = results.get("subscriptions", [])
  if not subscriptions:
    print("No subscriptions found.")
  else:
    print("Subscriptions:")
    for subscription in subscriptions:
      print(
          "{0} ({1}, {2})".format(
              subscription["customerId"],
              subscription["skuId"],
              subscription["plan"]["planName"],
          )
      )


if __name__ == "__main__":
  main()
# [END admin_sdk_reseller_quickstart]
