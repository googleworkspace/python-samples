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

import unittest

from base_test import BaseTest
from spreadsheet_snippets import SpreadsheetSnippets


class SpreadsheetSnippetsTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super(SpreadsheetSnippetsTest, cls).setUpClass()
        cls.snippets = SpreadsheetSnippets(cls.service)

    def test_create(self):
        spreadsheet_id = self.snippets.create('Title')
        self.assertIsNotNone(spreadsheet_id)
        self.delete_file_on_cleanup(spreadsheet_id)

    def test_batch_update(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        response = self.snippets.batch_update(spreadsheet_id,
                                              'New Title', 'Hello', 'Goodbye')
        self.assertIsNotNone(response)
        replies = response.get('replies')
        self.assertIsNotNone(replies)
        self.assertEqual(2, len(replies))
        find_replace_response = replies[1].get('findReplace')
        self.assertIsNotNone(find_replace_response)
        self.assertEqual(100, find_replace_response.get('occurrencesChanged'))

    def test_get_values(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        result = self.snippets.get_values(spreadsheet_id, 'A1:C2')
        self.assertIsNotNone(result)
        values = result.get('values')
        self.assertIsNotNone(values)
        self.assertEqual(2, len(values))
        self.assertEqual(3, len(values[0]))

    def test_batch_get_values(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        result = self.snippets.batch_get_values(spreadsheet_id,
                                                ['A1:A3', 'B1:C1'])
        self.assertIsNotNone(result)
        valueRanges = result.get('valueRanges')
        self.assertIsNotNone(valueRanges)
        self.assertEqual(2, len(valueRanges))
        values = valueRanges[0].get('values')
        self.assertEqual(3, len(values))

    def test_update_values(self):
        spreadsheet_id = self.create_test_spreadsheet()
        result = self.snippets.update_values(spreadsheet_id,
                                             'A1:B2', 'USER_ENTERED', [
                                                 ['A', 'B'],
                                                 ['C', 'D']
                                             ])
        self.assertIsNotNone(result)
        self.assertEqual(2, result.get('updatedRows'))
        self.assertEqual(2, result.get('updatedColumns'))
        self.assertEqual(4, result.get('updatedCells'))

    def test_batch_update_values(self):
        spreadsheet_id = self.create_test_spreadsheet()
        result = self.snippets.batch_update_values(spreadsheet_id,
                                                   'A1:B2', 'USER_ENTERED', [
                                                       ['A', 'B'],
                                                       ['C', 'D']
                                                   ])
        self.assertIsNotNone(result)
        self.assertEqual(1, len(result.get('responses')))
        self.assertEqual(2, result.get('totalUpdatedRows'))
        self.assertEqual(2, result.get('totalUpdatedColumns'))
        self.assertEqual(4, result.get('totalUpdatedCells'))

    def test_append_values(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        result = self.snippets.append_values(spreadsheet_id,
                                             'Sheet1', 'USER_ENTERED', [
                                                 ['A', 'B'],
                                                 ['C', 'D']
                                             ])
        self.assertIsNotNone(result)
        self.assertEqual('Sheet1!A1:J10', result.get('tableRange'))
        updates = result.get('updates')
        self.assertEqual('Sheet1!A11:B12', updates.get('updatedRange'))
        self.assertEqual(2, updates.get('updatedRows'))
        self.assertEqual(2, updates.get('updatedColumns'))
        self.assertEqual(4, updates.get('updatedCells'))

    def test_pivot_tables(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        response = self.snippets.pivot_tables(spreadsheet_id)
        self.assertIsNotNone(response)

    def test_conditional_formatting(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        response = self.snippets.conditional_formatting(spreadsheet_id)
        self.assertEqual(2, len(response.get('replies')))

    def test_filter_views(self):
        spreadsheet_id = self.create_test_spreadsheet()
        self.populate_values(spreadsheet_id)
        self.snippets.filter_views(spreadsheet_id)


if __name__ == '__main__':
    unittest.main()
