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

# [START forms_update_form]
from __future__ import print_function

from apiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

SCOPES = "https://www.googleapis.com/auth/forms.body"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"

store = file.Storage('token.json')
creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secrets.json', SCOPES)
    creds = tools.run_flow(flow, store)

form_service = discovery.build('forms', 'v1', http=creds.authorize(
    Http()), discoveryServiceUrl=DISCOVERY_DOC, static_discovery=False)

form = {
    "info": {
        "title": "Update metadata example for Forms API!",
    }
}

# Creates the initial Form
createResult = form_service.forms().create(body=form).execute()

# Request body to add description to a Form
update = {
    "requests": [{
        "updateFormInfo": {
            "info": {
                "description": "Please complete this quiz based on this week's readings for class."
            },
            "updateMask": "description"
        }
    }]
}

# Update the form with a description
question_setting = form_service.forms().batchUpdate(
    formId=createResult["formId"], body=update).execute()

# Print the result to see it now has a description
getresult = form_service.forms().get(formId=createResult["formId"]).execute()
print(getresult)
# [END forms_update_form]
