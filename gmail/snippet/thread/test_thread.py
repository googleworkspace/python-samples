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

from threads import show_chatty_threads


class TestThreads(unittest.TestCase):
  """unit test class for snippets"""

  @classmethod
  def test_threads(cls):
    """to test threads"""
    result = show_chatty_threads()
    cls.assertIsNotNone(cls, result)


if __name__ == "__main__":
  unittest.main()
