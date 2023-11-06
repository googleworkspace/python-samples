# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import unittest

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


class BaseTest(unittest.TestCase):
  RECIPIENT = "gduser01@workspacesamples.dev"
  TEST_USER = "ci-test01@workspacesamples.dev"
  FORWARDING_ADDRESS = "gduser01@workspacesamples.dev"

  @classmethod
  def setUpClass(cls):
    cls.service = cls.create_service()

  @classmethod
  def create_credentials(cls):
    scope = [
        "https://www.googleapis.com/auth/gmail.compose",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.labels",
        "https://www.googleapis.com/auth/gmail.settings.basic",
        "https://www.googleapis.com/auth/gmail.settings.sharing",
        "https://mail.google.com/",
    ]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        os.environ["SERVICE_ACCOUNT_CREDENTIALS"], scopes=scope
    )
    return credentials.create_delegated(BaseTest.TEST_USER)

  @classmethod
  def create_service(cls):
    credentials = cls.create_credentials()
    return discovery.build("gmail", "v1", credentials=credentials)


if __name__ == "__main__":
  unittest.main()
