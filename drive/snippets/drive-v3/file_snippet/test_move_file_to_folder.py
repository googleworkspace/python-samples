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

import move_file_to_folder


class TestMoveFileToFolder(unittest.TestCase):
    """Unit test class for file snippet"""

    @classmethod
    def test_move_file_to_folder(cls):
        """Test move_file_to_folder"""
        real_file_id = '1KuPmvGq8yoYgbfW74OENMCB5H0n_2Jm9'
        real_folder_id = '1v5eyIbXCr9TZX3eX_44HEExfe7yRj24V'

        update = move_file_to_folder.move_file_to_folder(
            real_file_id=real_file_id, real_folder_id=real_folder_id)
        cls.assertIsNotNone(cls, 0, len(update))


if __name__ == '__main__':
    unittest.main()
