# Copyright 2023 Google LLC
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


# [START chat_webhook_thread]
from json import dumps
from httplib2 import Http

# Copy the webhook URL from the Chat space where the webhook is registered.
# The values for SPACE_ID, KEY, and TOKEN are set by Chat, and are included
# when you copy the webhook URL.
#
# Then, append messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD to the
# webhook URL.


def main():
    """Google Chat incoming webhook that starts or replies to a message thread."""
    url = "https://chat.googleapis.com/v1/spaces/SPACE_ID/messages?key=KEY&token=TOKEN&messageReplyOption=REPLY_MESSAGE_FALLBACK_TO_NEW_THREAD"
    app_message = {
        "text": "Hello from a Python script!",
        # To start a thread, set threadKey to an arbitratry string.
        # To reply to a thread, specify that thread's threadKey value.
        "thread": {
            "threadKey": "THREAD_KEY_VALUE"
        },
    }
    message_headers = {"Content-Type": "application/json; charset=UTF-8"}
    http_obj = Http()
    response = http_obj.request(
        uri=url,
        method="POST",
        headers=message_headers,
        body=dumps(app_message),
    )
    print(response)


if __name__ == "__main__":
    main()
# [END chat_webhook_thread]
