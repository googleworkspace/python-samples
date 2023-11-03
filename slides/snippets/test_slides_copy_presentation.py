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

import slides_copy_presentation
from base_test import BaseTest


class TestCopyPresentation(BaseTest):
  """Unit test for Copy presentation  snippet"""

  def test_copy_presentation(self):
    """set title for copy presentation"""
    presentation_id = self.create_test_presentation()
    copy_id = slides_copy_presentation.copy_presentation(
        presentation_id, "My Duplicate Presentation"
    )
    self.assertIsNotNone(copy_id)
    self.delete_file_on_cleanup(copy_id)


if __name__ == "__main__":
  unittest.main()
