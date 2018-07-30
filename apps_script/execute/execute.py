# Copyright Google Inc.
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

# [START apps_script_execute]
from __future__ import print_function
from apiclient import errors
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file as oauthfile, client, tools

def main():
    """Shows basic usage of the Apps Script API.

    Creates a Apps Script API service object and uses it to call an
    Apps Script function to print out a list of folders in the user's root
    directory.
    """
    SCRIPT_ID = 'ENTER_YOUR_SCRIPT_ID_HERE'

    # Setup the Apps Script API
    SCOPES = 'https://www.googleapis.com/auth/script.projects'
    store = oauthfile.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('script', 'v1', http=creds.authorize(Http()))

    # Create an execution request object.
    request = {"function": "getFoldersUnderRoot"}

    try:
        # Make the API request.
        response = service.scripts().run(body=request,
                scriptId=SCRIPT_ID).execute()

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                        trace['lineNumber']))
        else:
            # The structure of the result depends upon what the Apps Script
            # function returns. Here, the function returns an Apps Script Object
            # with String keys and values, and so the result is treated as a
            # Python dictionary (folderSet).
            folderSet = response['response'].get('result', {})
            if not folderSet:
                print('No folders returned!')
            else:
                print('Folders under your root folder:')
                for (folderId, folder) in folderSet.iteritems():
                    print("\t{0} ({1})".format(folder, folderId))

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print(e.content)

if __name__ == '__main__':
    main()
# [END apps_script_execute]
