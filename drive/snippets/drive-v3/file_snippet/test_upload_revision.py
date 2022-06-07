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

import upload_revision


class TestUploadRevision(unittest.TestCase):
    """Unit test class for file snippet"""

    @classmethod
    def test_upload_revision(cls):
        """Test upload_revision"""

        real_file_id = '1KuPmvGq8yoYgbfW74OENMCB5H0n_2Jm9'
        file_id = upload_revision.upload_revision(real_file_id=real_file_id)
        cls.assertIsNotNone(cls, file_id)


if __name__ == '__main__':
    unittest.main()
