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
# It may require modifications to work in your environment.

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-apps-chat

# [START chat_list_messages_user_cred]
from authentication_utils import create_client_with_user_credentials
from google.apps import chat_v1 as google_chat

SCOPES = ["https://www.googleapis.com/auth/chat.messages.readonly"]

# This sample shows how to list messages with user credential
def list_messages_with_user_cred():
    # Create a client
    client = create_client_with_user_credentials(SCOPES)

    # Initialize request argument(s)
    request = google_chat.ListMessagesRequest(
        # Replace SPACE_NAME here
        parent = 'spaces/SPACE_NAME',
        # Number of results that will be returned at once
        page_size = 100
    )

    # Make the request
    page_result = client.list_messages(request)

    # Handle the response. Iterating over page_result will yield results and
    # resolve additional pages automatically.
    for response in page_result:
        print(response)

list_messages_with_user_cred()

# [END chat_list_messages_user_cred]
