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

from send_message_with_attachment import gmail_send_message_with_attachment


class TestSendMessageWithAttachment(unittest.TestCase):
  """Unit test class for gmail snippet"""

  def test_send_message_with_attachment(self):
    """test send message with attachment"""
    send_message = gmail_send_message_with_attachment()
    self.assertIsNotNone(self, send_message)


if __name__ == "__main__":
  unittest.main()
