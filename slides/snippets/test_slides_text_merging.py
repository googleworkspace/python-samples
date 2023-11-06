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

import slides_text_merging
from base_test import BaseTest


class TestTextMerging(BaseTest):
  """Unit test for SimpleTextReplace snippet"""

  TEMPLATE_PRESENTATION_ID = "10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4"
  DATA_SPREADSHEET_ID = "17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM"

  def test_text_merging(self):
    """text_merging method"""
    slides_text_merging.text_merging(
        self.TEMPLATE_PRESENTATION_ID, self.DATA_SPREADSHEET_ID
    )


if __name__ == "__main__":
  unittest.main()
