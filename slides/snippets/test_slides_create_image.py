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

import slides_create_image
from base_test import BaseTest


class TestCreateTextboxWithText(BaseTest):
  """Unit test case for create_image snippet"""

  def test_create_image(self):
    """presentation id and page id for create image"""
    presentation_id = self.create_test_presentation()
    page_id = self.add_slides(presentation_id, 1, "BLANK")[0]
    response = slides_create_image.create_image(presentation_id, page_id)
    self.assertEqual(1, len(response.get("replies")), msg=pformat(response))
    image_id = response.get("replies")[0].get("createImage").get("objectId")
    self.assertIsNotNone(image_id, msg=pformat(response))


if __name__ == "__main__":
  unittest.main()
