# Copyright 2018 Google LLC
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

from __future__ import print_function
import os
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from numpy import long

# If modifying these scopes, delete the file token.json.

SCOPES = ['https://www.googleapis.com/auth/gmail.settings.basic',
          'https://www.googleapis.com/auth/gmail.settings.sharing']


def main():
    """Shows basic usage settings snippets of gmail API.
        """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Gmail API service instance
        service = build('gmail', 'v1', credentials=creds)

        # Call update_signature function
        update_signature(service=service)
        # Call create_filter function
        create_filter(service=service)
        # Call enable_forwarding function
        enable_forwarding(service=service, real_forwarding_address='gduser2@workspacesamples.dev')
        # Call enable_auto reply function
        enable_auto_reply(service=service)

    except HttpError as error:
        print('An error occurred: %s' % error)


# [START gmail_updateSignature]
def update_signature(service):
    """Create and update signature in gmail.

    Args:
        service: Authorized Gmail API service instance.

    Returns:
        Draft object, including updated signature.
    """
    gmail_service = service
    primary_alias = None
    aliases = gmail_service.users().settings().sendAs().list(userId='me').execute()
    for alias in aliases.get('sendAs'):
        if alias.get('isPrimary'):
            primary_alias = alias
            break

    sendAsConfiguration = {
        'displayName': primary_alias.get('sendAsEmail'),
        'signature': 'Automated Signature'
    }
    result = gmail_service.users().settings().sendAs().patch(userId='me', sendAsEmail=primary_alias.get('sendAsEmail'),
                                                             body=sendAsConfiguration).execute()
    print('Updated signature for: %s' % result.get('displayName'))
    return result.get('signature')
# [END gmail_updateSignature]


# [START gmail_createFilter]
def create_filter(service):
    """Create a filter.

    Args:
        service: Authorized Gmail API service instance.

    Returns:
        Draft object, including filter id.
    """
    gmail_service = service
    label_name = 'IMPORTANT'
    filter = {
        'criteria': {
            'from': 'gsuder1@workspacesamples.dev'
        },
        'action': {
            'addLabelIds': [label_name],
            'removeLabelIds': ['INBOX']
        }
    }
    result = gmail_service.users().settings().filters().create(userId='me', body=filter).execute()
    print('Created filter with id: %s' % result.get('id'))
    return result.get('id')
# [END gmail_createFilter]


# [START gmail_enableForwarding]
def enable_forwarding(service, real_forwarding_address):
    """Enable email forwarding.

    Args:
        service: Authorized Gmail API service instance.
        real_forwarding_address: user's email address for forwarding

    Returns:
        Draft object, including forwarding id and result meta data.
    """
    gmail_service = service
    # address = { 'forwardingEmail': 'user2@example.com' }
    address = {'forwardingEmail': real_forwarding_address}
    result = gmail_service.users().settings().forwardingAddresses().create(userId='me', body=address).execute()
    if result.get('verificationStatus') == 'accepted':
        body = {
            'emailAddress': result.get('forwardingEmail'),
            'enabled': True,
            'disposition': 'trash'
        }
        result = gmail_service.users().settings().updateAutoForwarding(userId='me', body=body).execute()
        return result

    return None
# [END gmail_enableForwarding]


# [START gmail_enableAutoReply]
def enable_auto_reply(service):
    """Enable auto reply.

    Args:
        service: Authorized Gmail API service instance.

    Returns:
        Draft object, including reply message and response meta data.
    """
    gmail_service = service
    epoch = datetime.utcfromtimestamp(0)
    now = datetime.now()
    start_time = (now - epoch).total_seconds() * 1000
    end_time = (now + timedelta(days=7) - epoch).total_seconds() * 1000
    vacation_settings = {
        'enableAutoReply': True,
        'responseBodyHtml': "I am on vacation and will reply when I am "
                            "back in the office. Thanks!",
        'restrictToDomain': True,
        'startTime': long(start_time),
        'endTime': long(end_time)
    }
    response = gmail_service.users().settings().updateVacation(userId='me', body=vacation_settings).execute()
    print('Enabled Auto Reply with message: %s' % response.get('responseBodyHtml'))

    return response
# [END gmail_enableAutoReply]


if __name__ == '__main__':
    main()
