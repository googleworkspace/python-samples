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

import slides_create_textbox_with_text
from base_test import BaseTest


class TestCreateTextboxWithText(BaseTest):
  """Unit test for TestCreateTextboxWithText snippet"""

  def test_create_textbox_with_text(self):
    """Pass Presentation id and page id"""
    presentation_id = self.create_test_presentation()
    page_id = self.add_slides(presentation_id, 1, "BLANK")[0]
    response = slides_create_textbox_with_text.create_textbox_with_text(
        presentation_id, page_id
    )
    self.assertEqual(2, len(response.get("replies")), msg=pformat(response))
    box_id = response.get("replies")[0].get("createShape").get("objectId")
    self.assertIsNotNone(box_id, msg=pformat(response))


if __name__ == "__main__":
  unittest.main()
