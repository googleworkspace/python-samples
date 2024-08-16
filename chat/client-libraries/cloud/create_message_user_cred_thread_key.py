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

# [START chat_create_message_user_cred_thread_key]
from authentication_utils import create_client_with_user_credentials
from google.apps import chat_v1 as google_chat

import google.apps.chat_v1.CreateMessageRequest.MessageReplyOption

SCOPES = ["https://www.googleapis.com/auth/chat.messages.create"]

# This sample shows how to create message with user credential with thread key
def create_message_with_user_cred_thread_key():
    # Create a client
    client = create_client_with_user_credentials(SCOPES)

    # Initialize request argument(s)
    request = google_chat.CreateMessageRequest(
        # Replace SPACE_NAME here
        parent = "spaces/SPACE_NAME",
        # Creates the message as a reply to the thread specified by thread_key.
        # If it fails, the message starts a new thread instead.
        message_reply_option = MessageReplyOption.REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD,
        message = {
            "text": "Hello with user credential!",
            "thread": {
                # Thread key specifies a thread and is unique to the chat app
                # that sets it.
                "thread_key": "THREAD_KEY"
            }
        }
    )

    # Make the request
    response = client.create_message(request)

    # Handle the response
    print(response)

create_message_with_user_cred_thread_key()

# [END chat_create_message_user_cred_thread_key]
