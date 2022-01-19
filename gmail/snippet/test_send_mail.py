import unittest

import send_mail
from base_test import BaseTest


class SendMailTest(BaseTest):
    @classmethod
    def setUpClass(cls):
        super(SendMailTest, cls).setUpClass()

    def setUp(self):
        super(SendMailTest, self).setUp()

    def tearDown(self):
        super(SendMailTest, self).tearDown()

    def test_create_message(self):
        message = send_mail.create_message(SendMailTest.TEST_USER,
                                           SendMailTest.RECIPIENT,
                                           'Test',
                                           'Hello!')
        self.assertIsNotNone(message)  # Weak assertion

    def test_create_message_with_attachment(self):
        message = send_mail.create_message_with_attachment(SendMailTest.TEST_USER,
                                                           SendMailTest.RECIPIENT,
                                                           'Test',
                                                           'Hello!',
                                                           'files/photo.jpg')
        self.assertIsNotNone(message)  # Weak assertion

    def test_create_draft(self):
        message = send_mail.create_message(SendMailTest.TEST_USER,
                                           SendMailTest.RECIPIENT,
                                           'Test',
                                           'Hello!')
        draft = send_mail.create_draft(self.service, 'me', message)
        self.assertIsNotNone(draft)
        self.service.users().drafts().delete(userId='me', id=draft.get('id'))

    def test_send_mail(self):
        message = send_mail.create_message_with_attachment(SendMailTest.TEST_USER,
                                                           SendMailTest.RECIPIENT,
                                                           'Test',
                                                           'Hello!',
                                                           'files/photo.jpg')
        sent_message = send_mail.send_message(self.service, 'me', message)
        self.assertIsNotNone(sent_message)


if __name__ == '__main__':
    unittest.main()
