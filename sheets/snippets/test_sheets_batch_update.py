"""
Copyright 2022 Google LLC
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

import unittest

import sheets_batch_update
import sheets_create
from base_test import BaseTest


class Testbatchupdate(BaseTest):
  """Unit test class for Batch update Sheet snippet"""

  def test_batch_update(self):
    """test_batch_update function"""
    spreadsheet_id = sheets_create.create("Title")
    self.populate_values(spreadsheet_id)
    response = sheets_batch_update.sheets_batch_update(
        spreadsheet_id, "New Title", "Hello", "Goodbye"
    )
    self.assertIsNotNone(response)
    replies = response.get("replies")
    self.assertIsNotNone(replies)
    self.assertEqual(2, len(replies))
    find_replace_response = replies[1].get("findReplace")
    self.assertIsNotNone(find_replace_response)
    self.assertEqual(100, find_replace_response.get("occurrencesChanged"))


if __name__ == "__main__":
  unittest.main()
