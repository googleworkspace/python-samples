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

# [START chat_create_message_app_cred]
from authentication_utils import create_client_with_app_credentials
from google.apps import chat_v1 as google_chat

# This sample shows how to create message with app credential
def create_message_with_app_cred():
    # Create a client
    client = create_client_with_app_credentials()

    # Initialize request argument(s)
    request = google_chat.CreateMessageRequest(
        # Replace SPACE_NAME here.
        parent = "spaces/SPACE_NAME",
        message = {
            "text": '👋🌎 Hello world! I created this message by calling ' +
                    'the Chat API\'s `messages.create()` method.',
            "cards_v2" : [{ "card": {
                "header": {
                    "title": 'About this message',
                    "image_url": 'https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/info/default/24px.svg'
                },
                "sections": [{
                    "header": "Contents",
                    "widgets": [{ "text_paragraph": {
                            "text": '🔡 <b>Text</b> which can include ' +
                                    'hyperlinks 🔗, emojis 😄🎉, and @mentions 🗣️.'
                        }}, { "text_paragraph": {
                            "text": '🖼️ A <b>card</b> to display visual elements' +
                                    'and request information such as text 🔤, ' +
                                    'dates and times 📅, and selections ☑️.'
                        }}, { "text_paragraph": {
                            "text": '👉🔘 An <b>accessory widget</b> which adds ' +
                                    'a button to the bottom of a message.'
                        }}
                    ]}, {
                        "header": "What's next",
                        "collapsible": True,
                        "widgets": [{ "text_paragraph": {
                                "text": "❤️ <a href='https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages.reactions/create'>Add a reaction</a>."
                            }}, { "text_paragraph": {
                                "text": "🔄 <a href='https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/patch'>Update</a> " +
                                        "or ❌ <a href='https://developers.google.com/workspace/chat/api/reference/rest/v1/spaces.messages/delete'>delete</a> " +
                                        "the message."
                            }
                        }]
                    }
                ]
            }}],
            "accessory_widgets": [{ "button_list": { "buttons": [{
                "text": 'View documentation',
                "icon": { "material_icon": { "name": 'link' }},
                "on_click": { "open_link": {
                    "url": 'https://developers.google.com/workspace/chat/create-messages'
                }}
            }]}}]
        }
    )

    # Make the request
    response = client.create_message(request)

    # Handle the response
    print(response)

create_message_with_app_cred()

# [END chat_create_message_app_cred]
