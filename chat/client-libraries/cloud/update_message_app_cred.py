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

# [START chat_update_message_app_cred]
from authentication_utils import create_client_with_app_credentials
from google.apps import chat_v1 as google_chat

# This sample shows how to update a message with app credential
def update_message_with_app_cred():
    # Create a client
    client = create_client_with_app_credentials()

    # Initialize request argument(s)
    request = google_chat.UpdateMessageRequest(
        message = {
            # Replace SPACE_NAME and MESSAGE_NAME here
            "name": "spaces/SPACE_NAME/messages/MESSAGE_NAME",
            "text": "Text updated with app credential!",
            "cards_v2" : [{ "card": { "header": {
                "title": 'Card updated with app credential!',
                "image_url": 'https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/info/default/24px.svg'
            }}}]
        },
        # The field paths to update. Separate multiple values with commas or use
        # `*` to update all field paths.
        update_mask = "text,cardsV2"
    )

    # Make the request
    response = client.update_message(request)

    # Handle the response
    print(response)

update_message_with_app_cred()

# [END chat_update_message_app_cred]
