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

from update_smime_from_csv import update_smime_from_csv


class TestUpdateSmimeFromCsv(unittest.TestCase):
  """unit test class for snippets"""

  @classmethod
  def test_update_smime_from_csv(cls):
    """test to update smime from csv"""
    result = update_smime_from_csv(csv_filename="abc")
    cls.assertIsNotNone(cls, result)


if __name__ == "__main__":
  unittest.main()
