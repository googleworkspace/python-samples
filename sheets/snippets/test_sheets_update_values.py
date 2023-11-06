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

import sheets_update_values
from base_test import BaseTest


class Testupdatesvalues(BaseTest):
  """Unit test for update value Sheet snippet"""

  def test_update_values(self):
    """test updates_values"""
    spreadsheet_id = self.create_test_spreadsheet()
    result = sheets_update_values.update_values(
        spreadsheet_id, "A1:B2", "USER_ENTERED", [["A", "B"], ["C", "D"]]
    )
    self.assertIsNotNone(result)
    self.assertEqual(2, result.get("updatedRows"))
    self.assertEqual(2, result.get("updatedColumns"))
    self.assertEqual(4, result.get("updatedCells"))


if __name__ == "__main__":
  unittest.main()
