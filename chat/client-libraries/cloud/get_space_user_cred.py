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
# Snippet for GetSpace

# To install the latest published package dependency, execute the following:
#   python3 -m pip install google-apps-chat

# [START chat_get_space_user_cred]
from authentication_utils import create_client_with_user_credentials
from google.apps import chat_v1 as google_chat

SCOPES = ["https://www.googleapis.com/auth/chat.spaces.readonly"]

# This sample shows how to get space with user credential
def get_space_with_user_cred():
    # Create a client
    client = create_client_with_user_credentials(SCOPES)

    # Initialize request argument(s)
    request = google_chat.GetSpaceRequest(
        # Replace SPACE_NAME here
        name = "spaces/SPACE_NAME",
    )

    # Make the request
    response = client.get_space(request)

    # Handle the response
    print(response)

get_space_with_user_cred()

# [END chat_get_space_user_cred]
