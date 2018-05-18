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

# [START admin_sdk_groups_settings_quickstart]
"""
Shows basic usage of the Admin SDK Groups Settings API. Outputs a group's
settings identified by the group's email address.
"""

"""
Outputs all the groups in the domain which have 'external' to the domain access.
Also outputs their access settings.
"""
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/group-settings-public.json
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
  home_dir = os.path.expanduser('~')
  credential_dir = os.path.join(home_dir, '.credentials')
  if not os.path.exists(credential_dir):
      os.makedirs(credential_dir)
  credential_path = os.path.join(credential_dir,
                                 'group-settings-public.json')

  store = Storage(credential_path)
  credentials = store.get()
  if not credentials or credentials.invalid:
      flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
      flow.user_agent = APPLICATION_NAME
      if flags:
          credentials = tools.run_flow(flow, store, flags)
      else: # Needed only for compatibility with Python 2.6
          credentials = tools.run(flow, store)
      print('Storing credentials to ' + credential_path)
  return credentials


def print_if_external_access_enabled(groupEmail, settings):
  """
  Given the group email and its settings, checks some of its settings and prints
  them if the group has external access.
  """
  whoCanViewGroup = settings['whoCanViewGroup']
  whoCanJoin = settings['whoCanJoin']
  allowExternalMembers = settings['allowExternalMembers']
  whoCanPostMessage = settings['whoCanPostMessage']
  whoCanViewMembership = settings['whoCanViewMembership']
  if (whoCanViewGroup == ANYONE_CAN_VIEW_GROUP
      or whoCanJoin == ANYONE_CAN_JOIN_GROUP
      or allowExternalMembers == EXTERNAL_MEMBERS_CAN_JOIN
      or whoCanPostMessage == ANYONE_CAN_POST_MESSAGE
      or whoCanViewMembership == ANYONE_CAN_VIEW_MEMBERSHIP):
    print(groupEmail)
    print('    whoCanViewGroup - {0}'.format(whoCanViewGroup))
    print('    whoCanJoin - {0}'.format(whoCanJoin))
    print('    allowExternalMembers - {0}'.format(allowExternalMembers))
    print('    whoCanPostMessage - {0}'.format(whoCanPostMessage))
    print('    whoCanViewMembership - {0}'.format(whoCanViewMembership))


def get_group_settings(group_settings_service, groupEmail):
  """
  Gets the group settings for the given groupEmail and prints the group
  if it has external access enabled.
  """
  try:
    settings = group_settings_service.groups().get(
        groupUniqueId=groupEmail).execute()
    print_if_external_access_enabled(groupEmail, settings)
  except:
    print('Unable to read group: {0}'.format(groupEmail))


def get_groups(group_service, group_settings_service, pageToken):
  """
  Gets the groups in the domain, gets group settings for each group and prints
  the ones which have external access enabled.

  Returns:
      pageToken to get the next page of groups
  """
  results = group_service.groups().list(
      customer='my_customer', pageToken=pageToken, orderBy='email').execute()
  groups = results.get('groups', [])

  if groups:
    for group in groups:
      get_group_settings(group_settings_service, group['email'])
  return results.get('nextPageToken', None)


def main():
  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  group_service = discovery.build('admin', 'directory_v1', http=http)
  group_settings_service = discovery.build('groupssettings', 'v1', http=http)

  pageToken = None
  while True:
    pageToken = get_groups(group_service=group_service,
                           group_settings_service=group_settings_service,
                           pageToken=pageToken)
    if pageToken is None:
      break

if __name__ == '__main__':
  main()
