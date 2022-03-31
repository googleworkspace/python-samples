"""
Copyright 2018 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# [START calendar_quickstart]
from __future__ import print_function

import datetime

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def main():
    """
    Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    The file token.json stores the user's access and refresh tokens, and is
    created automatically when the authorization flow completes for the first
    time.
    """

    creds, _ = google.auth.default()

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Call the Calendar API
        # pylint: disable=no-member
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates
        # UTC time
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='primary',
                                              timeMin=now,
                                              maxResults=10,
                                              singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        # Prints the start and name of the next 10 events
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == '__main__':
    main()
# [END calendar_quickstart]
