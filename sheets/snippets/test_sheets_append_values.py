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

import sheets_append_values
from base_test import BaseTest


class Testappendvalues(BaseTest):
  """Unit test for append value Sheet snippet"""

  def test_append_values(self):
    """test append values function"""
    spreadsheet_id = self.create_test_spreadsheet()
    self.populate_values(spreadsheet_id)
    result = sheets_append_values.append_values(
        spreadsheet_id, "Sheet1", "USER_ENTERED", [["A", "B"], ["C", "D"]]
    )
    self.assertIsNotNone(result)
    self.assertEqual("Sheet1!A1:J10", result.get("tableRange"))
    updates = result.get("updates")
    self.assertEqual("Sheet1!A11:B12", updates.get("updatedRange"))
    self.assertEqual(2, updates.get("updatedRows"))
    self.assertEqual(2, updates.get("updatedColumns"))
    self.assertEqual(4, updates.get("updatedCells"))


if __name__ == "__main__":
  unittest.main()
