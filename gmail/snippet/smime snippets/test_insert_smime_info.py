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

from insert_smime_info import insert_smime_info


class TestInsertSmimeInfo(unittest.TestCase):
  """Unit test class for snippet"""

  @classmethod
  def test_insert_smime_info(cls):
    """test to insert smime info"""
    result = insert_smime_info()
    cls.assertIsNotNone(cls, result)


if __name__ == "__main__":
  unittest.main()
