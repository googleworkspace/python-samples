# Copyright 2021 Google LLC
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

# [START forms_create_watch]
from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/drive"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage("token.json")
creds = None
if not creds or creds.invalid:
  flow = client.flow_from_clientsecrets("client_secret.json", SCOPES)
  creds = tools.run_flow(flow, store)

service = discovery.build(
    "forms",
    "v1",
    http=creds.authorize(Http()),
    discoveryServiceUrl=DISCOVERY_DOC,
    static_discovery=False,
)

watch = {
    "watch": {
        "target": {"topic": {"topicName": "<YOUR_TOPIC_PATH>"}},
        "eventType": "RESPONSES",
    }
}

form_id = "<YOUR_FORM_ID>"

# Print JSON response after form watch creation
result = service.forms().watches().create(formId=form_id, body=watch).execute()
print(result)
# [END forms_create_watch]
