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
print_group_settingss all the groups in the domain which have 'external' to the domain access.
Also print_group_settingss their access settings.
"""
from __future__ import print_function
import httplib2

from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage

# If modifying these scopes, delete your previously saved credentials
# at credentials.json
SCOPES = ['https://www.googleapis.com/auth/admin.directory.group',
          'https://www.googleapis.com/auth/apps.groups.settings']
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'List Groups with external access'

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

def get_credentials():
    """Gets valid user credentials from storage.

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

def print_group_settings(group_email, settings):
    """
    Given the group email and its settings, checks some of its settings and
    prints them if the group has external access.
    """
    who_can_view_group = settings['whoCanViewGroup']
    who_can_join = settings['whoCanJoin']
    allow_external_members = settings['allowExternalMembers']
    who_can_post_message = settings['whoCanPostMessage']
    who_can_view_membership = settings['whoCanViewMembership']
    if (who_can_view_group == ANYONE_CAN_VIEW_GROUP
            or who_can_join == ANYONE_CAN_JOIN_GROUP
            or allow_external_members == EXTERNAL_MEMBERS_CAN_JOIN
            or who_can_post_message == ANYONE_CAN_POST_MESSAGE
            or who_can_view_membership == ANYONE_CAN_VIEW_MEMBERSHIP):
        print(group_email)
        print('\twhoCanViewGroup - {0}'.format(who_can_view_group))
        print('\twhoCanJoin - {0}'.format(who_can_join))
        print('\tallowExternalMembers - {0}'.format(allow_external_members))
        print('\twhoCanPostMessage - {0}'.format(who_can_post_message))
        print('\twhoCanViewMembership - {0}'.format(who_can_view_membership))

def check_group_settings(group_settings_service, group_email):
    """
    Gets the group settings for the given group_email and prints the group
    if it has external access enabled.
    """
    try:
        settings = group_settings_service.groups().get(
            groupUniqueId=group_email).execute()
        print_group_settings(group_email, settings)
    except errors.HttpError:
        print('Unable to read group: {0}'.format(group_email))

def check_groups(group_service, group_settings_service, page_token):
    """
    Gets the groups in the domain, gets group settings for each group and prints
    the ones which have external access enabled.

    Returns:
            page_token to get the next page of groups
    """
    results = group_service.groups().list(customer='my_customer',
                                          pageToken=page_token,
                                          orderBy='email').execute()
    groups = results.get('groups', [])

    if groups:
        for group in groups:
            check_group_settings(group_settings_service, group['email'])
    return results.get('nextPageToken', None)

def main():
    """
    Runs the script.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    group_service = discovery.build('admin', 'directory_v1', http=http)
    group_settings_service = discovery.build('groupssettings', 'v1', http=http)

    page_token = None
    while True:
        page_token = check_groups(group_service=group_service,
                                  group_settings_service=group_settings_service,
                                  page_token=page_token)
        if page_token is None:
            break

if __name__ == '__main__':
    main()
