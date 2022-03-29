"""
Copyright Google Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# [START apps_script_api_execute]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    """Runs the sample.
    """
    # pylint: disable=maybe-no-member
    script_id = '1VFBDoJFy6yb9z7-luOwRv3fCmeNOzILPnR4QVmR0bGJ7gQ3QMPpCW-yt'

    creds, _ = google.auth.default()
    service = build('script', 'v1', credentials=creds)

    # Create an execution request object.
    request = {"function": "getFoldersUnderRoot"}

    try:
        # Make the API request.
        response = service.scripts().run(scriptId=script_id,
                                         body=request).execute()
        if 'error' in response:
            # The API executed, but the script returned an error.
            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # a list of stack trace elements.
            error = response['error']['details'][0]
            print(f"Script error message: {0}.{format(error['errorMessage'])}")

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print(f"\t{0}: {1}."
                          f"{format(trace['function'], trace['lineNumber'])}")
        else:
            # The structure of the result depends upon what the Apps Script
            # function returns. Here, the function returns an Apps Script
            # Object with String keys and values, and so the result is
            # treated as a Python dictionary (folder_set).
            folder_set = response['response'].get('result', {})
            if not folder_set:
                print('No folders returned!')
            else:
                print('Folders under your root folder:')
                for (folder_id, folder) in folder_set.items():
                    print(f"\t{0} ({1}).{format(folder, folder_id)}")

    except HttpError as error:
        # The API encountered a problem before the script started executing.
        print(f"An error occurred: {error}")
        print(error.content)


if __name__ == '__main__':
    main()
# [END apps_script_api_execute]
