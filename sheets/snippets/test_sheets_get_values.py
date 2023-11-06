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

import sheets_get_values
from base_test import BaseTest


class Testgetvalues(BaseTest):
  """Unit test class for get value Sheet snippet"""

  def test_get_values(self):
    """test_get_values"""
    spreadsheet_id = self.create_test_spreadsheet()
    self.populate_values(spreadsheet_id)
    result = sheets_get_values.get_values(spreadsheet_id, "A1:C2")
    self.assertIsNotNone(result)
    values = result.get("values")
    self.assertIsNotNone(values)
    self.assertEqual(2, len(values))
    self.assertEqual(3, len(values[0]))


if __name__ == "__main__":
  unittest.main()
