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

import slides_create_slide
from base_test import BaseTest


class TestCreateSlide(BaseTest):
  """Unit test for create Slide  snippet"""

  def test_create_slide(self):
    """pass presentation_id and page_id for creating the slides"""
    presentation_id = self.create_test_presentation()
    self.add_slides(presentation_id, 3)
    page_id = "my_page_id"
    response = slides_create_slide.create_slide(presentation_id, page_id)
    self.assertEqual(
        page_id,
        response.get("replies")[0].get("createSlide").get("objectId"),
    )


if __name__ == "__main__":
  unittest.main()
