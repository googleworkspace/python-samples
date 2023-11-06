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

import slides_create_presentation
from base_test import BaseTest


class TestCreatePresentation(BaseTest):
  """Unit test for create presentation  snippet"""

  def test_create_presentation(self):
    """Set title for create presentation"""
    presentation = slides_create_presentation.create_presentation("Title")
    self.assertIsNotNone(presentation)
    self.delete_file_on_cleanup(presentation.get("presentationId"))


if __name__ == "__main__":
  unittest.main()
