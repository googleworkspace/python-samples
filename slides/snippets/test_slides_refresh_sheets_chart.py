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
from pprint import pformat

import slides_refresh_sheets_chart
from base_test import BaseTest


class TestCreateSheetsChart(BaseTest):
  """Unit test for refresh_sheets_chart snippet"""

  DATA_SPREADSHEET_ID = "17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM"
  CHART_ID = 1107320627

  def test_refresh_sheets_chart(self):
    """refresh_sheets_chart method"""
    presentation_id = self.create_test_presentation()
    page_id = self.add_slides(presentation_id, 1, "BLANK")[0]
    chart_id = self.create_test_sheets_chart(
        presentation_id, page_id, self.DATA_SPREADSHEET_ID, self.CHART_ID
    )
    response = slides_refresh_sheets_chart.refresh_sheets_chart(
        presentation_id, chart_id
    )
    self.assertEqual(1, len(response.get("replies")), msg=pformat(response))


if __name__ == "__main__":
  unittest.main()
