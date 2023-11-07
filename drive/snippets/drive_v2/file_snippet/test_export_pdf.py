"""Copyright 2022 Google LLC

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

from .export_pdf import export_pdf


class TestExportPdf(unittest.TestCase):
  """Unit test class for file snippet"""

  def test_export_pdf(self):
    """Test export_pdf"""
    # valid file ID
    real_file_id = "1zbp8wAyuImX91Jt9mI-CAX_1TqkBLDEDcr2WeXBbKUY"
    file = export_pdf(real_file_id=real_file_id)
    self.assertNotEqual(0, len(file))


if __name__ == "__main__":
  unittest.main()
