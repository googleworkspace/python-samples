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

import search_file


class TestSearchFile(unittest.TestCase):
    """Unit test class for file snippet"""

    @classmethod
    def test_search_file(cls):
        """Test search_file"""
        file = search_file.search_file()
        cls.assertNotEqual(cls, 0, len(file))


if __name__ == '__main__':
    unittest.main()
