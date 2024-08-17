# -*- coding: utf-8 -*-
# Copyright 2024 Google LLC
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
#
# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-apps-chat

# [START chat_authentication_utils]
import json

import google.oauth2.credentials

from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import chat_v1 as google_chat

CLIENT_SECRETS_FILE = 'client_secrets.json'

SERVICE_ACCOUNT_FILE = 'service_account.json'

APP_AUTH_OAUTH_SCOPE = ["https://www.googleapis.com/auth/chat.bot"]

def create_client_with_app_credentials():
    # For more information on app authentication, see
    # https://developers.google.com/workspace/chat/authenticate-authorize-chat-app
    creds = google.oauth2.service_account.Credentials.from_service_account_file(
                SERVICE_ACCOUNT_FILE)

    return google_chat.ChatServiceClient(
            credentials = creds,
            client_options={
                "scopes": APP_AUTH_OAUTH_SCOPE
            })

def create_client_with_user_credentials(scopes):
    # For more information on user authentication, see
    # https://developers.google.com/workspace/chat/authenticate-authorize-chat-user
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes)
    cred = flow.run_local_server()
    installed = json.load(open(CLIENT_SECRETS_FILE))["installed"]

    creds = google.oauth2.credentials.Credentials(
            token = cred.token,
            refresh_token = cred.refresh_token,
            token_uri = installed["token_uri"],
            client_id = installed["client_id"],
            client_secret = installed["client_secret"],
            scopes = scopes
    )

    # Create a client
    client = google_chat.ChatServiceClient(
            credentials = creds,
            client_options = {
                "scopes" : scopes
            }
    )

    return client

# [END chat_authentication_utils]
