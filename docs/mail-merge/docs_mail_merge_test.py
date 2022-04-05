# -*- coding: utf-8 -*-
#
# Copyright ©2018-2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at apache.org/licenses/LICENSE-2.0.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
docs_mail_merge_test.py -- unit test for docs_mail_merge.py:
    1. test credentials file availability
    2. test whether project can connect to all 3 APIs
    3. test creation (and deletion) of Google Docs file
    4. test copying (and deletion) of Google Docs file
    5. test getting plain text data
    6. test getting data from Google Sheets spreadsheet
"""

import unittest

import google.auth
from docs_mail_merge import _copy_template, get_data
from googleapiclient import discovery

creds, _ = google.auth.default()


class TestDocsMailMerge(unittest.TestCase):
    'Unit tests for Mail Merge sample'

    def test_project(self):
        self.assertTrue(project_test())

    def test_create_doc(self):
        self.assertTrue(create_doc_test())

    def test_copy_doc(self):
        self.assertTrue(copy_doc_test())

    def test_get_text_data(self):
        self.assertTrue(bool(get_text_data_test()))

    def test_get_sheets_data(self):
        self.assertTrue(bool(get_sheets_data_test()))


def project_test():
    'Tests whether project credentials file was downloaded from project.'
    credentials, project = google.auth.default()


def create_doc_test():
    'Tests whether project can create and delete a Google Docs file.'
    DRIVE = discovery.build('drive', 'v3', credentials=creds)
    DATA = {
        'name': 'Test Doc',
        'mimeType': 'application/vnd.google-apps.document',
    }
    doc_id = DRIVE.files().create(body=DATA, fields='id').execute().get('id')
    DRIVE.files().delete(fileId=doc_id, fields='').execute()
    return True


def copy_doc_test():
    'Tests whether project can copy and delete a Google Docs file.'
    DRIVE = discovery.build('drive', 'v3', credentials=creds)
    DOCS_FILE_ID = '1Xycxuuv7OhEQUuzbt_Mw0TPMq02MseSD1vZdBJ3nLjk'
    doc_id = _copy_template(DOCS_FILE_ID, 'text', DRIVE)
    DRIVE.files().delete(fileId=doc_id, fields='').execute()
    return True


def get_text_data_test():
    'Tests reading plain text data.'
    return get_data('text')


def get_sheets_data_test():
    'Tests reading Google Sheets data.'
    return get_data('sheets')


if __name__ == '__main__':
    unittest.main()
