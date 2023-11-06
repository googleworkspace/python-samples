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

import slides_create_bulleted_text
from base_test import BaseTest


class TestCreateBulletedText(BaseTest):
  """Unit test for create_bulleted_text snippet"""

  def test_create_bulleted_text(self):
    """create_bulleted_text function"""
    presentation_id = self.create_test_presentation()
    page_id = self.add_slides(presentation_id, 1, "BLANK")[0]
    box_id = self.create_test_textbox(presentation_id, page_id)
    response = slides_create_bulleted_text.create_bulleted_text(
        presentation_id, box_id
    )
    self.assertEqual(1, len(response.get("replies")), msg=pformat(response))


if __name__ == "__main__":
  unittest.main()
