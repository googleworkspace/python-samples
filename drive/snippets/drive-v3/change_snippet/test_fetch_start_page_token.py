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

import fetch_start_page_token


class TestFetchChanges(unittest.TestCase):
    """Unit test classs for Change snippet"""

    @classmethod
    def test_fetch_start_page_token(cls):
        """Test fetch_start_page_token"""
        token = fetch_start_page_token.fetch_start_page_token()
        cls.assertIsNotNone(cls, token)


if __name__ == '__main__':
    unittest.main()
