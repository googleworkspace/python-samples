# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Updates the access settings of a Group to domain internal.

Access settings include
  whoCanViewGroup
  whoCanJoin
  allowExternalMembers
  whoCanPostMessage
  whoCanViewMembership

Only the setting which is domain external will be updated. Rest will stay as is.
"""
from __future__ import print_function
import httplib2

from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at credentials.json
SCOPES = 'https://www.googleapis.com/auth/apps.groups.settings'

# External access for view group
ANYONE_CAN_VIEW_GROUP = 'ANYONE_CAN_VIEW'

# External access for who can join
ANYONE_CAN_JOIN_GROUP = 'ANYONE_CAN_JOIN'

# Group can have external members
EXTERNAL_MEMBERS_CAN_JOIN = 'true'

# External access for who can post messages
ANYONE_CAN_POST_MESSAGE = 'ANYONE_CAN_POST'

# External access for who can view members
ANYONE_CAN_VIEW_MEMBERSHIP = 'ANYONE_CAN_VIEW'

# Domain access for view group
DOMAIN_CAN_VIEW_GROUP = 'ALL_IN_DOMAIN_CAN_VIEW'

# Domain access for who can join
DOMAIN_CAN_JOIN_GROUP = 'ALL_IN_DOMAIN_CAN_JOIN'

# Group cannot have external members
EXTERNAL_MEMBERS_CANNOT_JOIN = 'false'

# Domain access for who can post messages
DOMAIN_CAN_POST_MESSAGE = 'ALL_IN_DOMAIN_CAN_POST'

# Domain access for who can view members
DOMAIN_CAN_VIEW_MEMBERSHIP = 'ALL_IN_DOMAIN_CAN_VIEW'

def get_credentials():
    """
    Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    store = Storage('credentials.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return creds

def update_group_to_domain(group_settings_service, group_email):
    """
    Gets the settings for the given group, and updates the access settings
    if any of them were external.
    """
    try:
        settings = group_settings_service.groups().get(
            groupUniqueId=group_email).execute()
        who_can_view_group = settings['whoCanViewGroup']
        who_can_join = settings['whoCanJoin']
        allow_external_members = settings['allowExternalMembers']
        who_can_post_message = settings['whoCanPostMessage']
        who_can_view_membership = settings['whoCanViewMembership']
        updated_settings = {}
        if who_can_view_group == ANYONE_CAN_VIEW_GROUP:
            updated_settings['whoCanViewGroup'] = DOMAIN_CAN_VIEW_GROUP
        if who_can_join == ANYONE_CAN_JOIN_GROUP:
            updated_settings['whoCanJoin'] = DOMAIN_CAN_JOIN_GROUP
        if allow_external_members == EXTERNAL_MEMBERS_CAN_JOIN:
            updated_settings['allowExternalMembers'] = EXTERNAL_MEMBERS_CANNOT_JOIN
        if who_can_post_message == ANYONE_CAN_POST_MESSAGE:
            updated_settings['whoCanPostMessage'] = DOMAIN_CAN_POST_MESSAGE
        if who_can_view_membership == ANYONE_CAN_VIEW_MEMBERSHIP:
            updated_settings['whoCanViewMembership'] = DOMAIN_CAN_VIEW_MEMBERSHIP

        if bool(updated_settings):
            try:
                group_settings_service.groups().update(
                    groupUniqueId=group_email, body=updated_settings).execute()
                print('Updated settings of {0} to {1}'.format(
                    group_email, updated_settings))
            except errors.HttpError:
                print('Could not update settings')
        else:
            print('Nothing to update')
    except errors.HttpError:
        print('Unable to read group: {0}'.format(group_email))

def main():
    """
    Prompts the user for an email address for the domain Group.
    Updates group access settings.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    group_settings_service = discovery.build('groupssettings', 'v1', http=http)
    group_email = raw_input('Enter the email address of the Group in your'
                            'domain, that you want to update: ')
    update_group_to_domain(group_settings_service, group_email)

if __name__ == '__main__':
    main()
