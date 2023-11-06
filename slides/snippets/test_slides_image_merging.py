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

import slides_image_merging
from base_test import BaseTest


class TestTextMerging(BaseTest):
  """Unit test for text merging snippet"""

  TEMPLATE_PRESENTATION_ID = "10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4"
  DATA_SPREADSHEET_ID = "17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM"
  IMAGE_URL = "https://picsum.photos/200"
  CHART_ID = 1107320627
  CUSTOMER_NAME = "Fake Customer"

  def test_image_merging(self):
    """image merging function"""
    response = slides_image_merging.image_merging(
        self.TEMPLATE_PRESENTATION_ID, self.IMAGE_URL, self.CUSTOMER_NAME
    )
    presentation_id = response.get("presentationId")
    self.delete_file_on_cleanup(presentation_id)
    self.assertIsNotNone(presentation_id, msg=pformat(response))
    self.assertEqual(2, len(response.get("replies")), msg=pformat(response))
    num_replacements = 0
    for reply in response.get("replies"):
      if isinstance(reply, int):
        num_replacements += reply.get("replaceAllShapesWithImage").get(
            "occurrencesChanged"
        )


if __name__ == "__main__":
  unittest.main()
