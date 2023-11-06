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

import slides_simple_text_replace
from base_test import BaseTest


class TestSimpleTextReplace(BaseTest):
  """Unit test for SimpleTextReplace snippet"""

  def test_simple_text_replace(self):
    """test_simple_text_replace function"""
    presentation_id = self.create_test_presentation()
    page_id = self.add_slides(presentation_id, 1, "BLANK")[0]
    box_id = self.create_test_textbox(presentation_id, page_id)
    response = slides_simple_text_replace.simple_text_replace(
        presentation_id, box_id, "MY NEW TEXT"
    )
    self.assertEqual(2, len(response.get("replies")), msg=pformat(response))


if __name__ == "__main__":
  unittest.main()
