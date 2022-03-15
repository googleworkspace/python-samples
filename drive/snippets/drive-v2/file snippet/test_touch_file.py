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
import re
import unittest
from datetime import datetime

import touch_file


class TestTouchFile(unittest.TestCase):
    """Unit test class for file snippet"""

    @classmethod
    def test_touch_file(cls):
        """Test touch_file"""
        real_file_id = '1KuPmvGq8yoYgbfW74OENMCB5H0n_2Jm9'
        now = datetime.utcnow().isoformat() + 'Z'
        now = re.sub(r'\d{3}Z', 'Z', now)  # Truncate microseconds
        modified_time = touch_file.touch_file(real_file_id=real_file_id,
                                              real_timestamp=now)
        cls.assertIsNotNone(cls, modified_time)


if __name__ == '__main__':
    unittest.main()
