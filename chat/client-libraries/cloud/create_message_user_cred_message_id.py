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


# [START chat_create_message_user_cred_message_id]
from authentication_utils import create_client_with_user_credentials
from google.apps import chat_v1 as google_chat

SCOPES = ["https://www.googleapis.com/auth/chat.messages.create"]

# This sample shows how to create message with user credential with message id
def create_message_with_user_cred_message_id():
    # Create a client
    client = create_client_with_user_credentials(SCOPES)

    # Initialize request argument(s)
    request = google_chat.CreateMessageRequest(
        # Replace SPACE_NAME here
        parent = "spaces/SPACE_NAME",
        # Message id let chat apps get, update or delete a message without needing
        # to store the system assigned ID in the message's resource name.
        message_id = "client-MESSAGE-ID",
        message = {
            "text": "Hello with user credential!"
        }
    )

    # Make the request
    response = client.create_message(request)

    # Handle the response
    print(response)

create_message_with_user_cred_message_id()

# [END chat_create_message_user_cred_message_id]
