import datetime
import unittest
from unittest import mock

import httplib2
import smime_snippets
from apiclient import errors


class SmimeSnippetsTest(unittest.TestCase):
    CURRENT_TIME = 1234567890
    TEST_USER = 'user1@example.com'

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.mock_delete = mock.Mock()
        self.mock_get = mock.Mock()
        self.mock_insert = mock.Mock()
        self.mock_list = mock.Mock()
        self.mock_set_default = mock.Mock()

        self.mock_service = mock.Mock()
        self.mock_service.users.return_value = self.mock_service
        self.mock_service.settings.return_value = self.mock_service
        self.mock_service.sendAs.return_value = self.mock_service
        self.mock_service.smimeInfo.return_value = self.mock_service

        self.mock_service.delete = self.mock_delete
        self.mock_service.get = self.mock_get
        self.mock_service.insert = self.mock_insert
        self.mock_service.list = self.mock_list
        self.mock_service.setDefault = self.mock_set_default

    def tearDown(self):
        # The delete() and get() API methods are not used and should not be called.
        self.mock_delete.assert_not_called()
        self.mock_get.assert_not_called()

    @staticmethod
    def make_fake_insert_result(id='new_certificate_id',
                                is_default=False,
                                expiration=CURRENT_TIME + 1):
        """Construct a fake result of calling insert() on the S/MIME API.

        By default, the certificate expires after CURRENT_TIME.
        """
        return {
            'id': id,
            'isDefault': is_default,
            'expiration': expiration * 1000,
            'issuerCn': 'fake_authority',
            'pem': 'fake_certificate_contents',
        }

    def make_fake_list_result(self,
                              is_default=[False],
                              expiration=[CURRENT_TIME + 1]):
        """Construct a fake result of calling list() on the S/MIME API.

        No more than one of the values in is_default may be True.
        By default, each certificate expires after CURRENT_TIME.
        """
        self.assertEqual(len(is_default), len(expiration))
        self.assertLessEqual(is_default.count(True), 1)
        smime_info = []
        id_base = 'existing_certificate_id_%d'
        for i in range(len(is_default)):
            smime_info.append(
                self.make_fake_insert_result(
                    id=(id_base % i),
                    is_default=is_default[i],
                    expiration=expiration[i]))
        return {'smimeInfo': smime_info}

    @staticmethod
    def make_http_error(status, reason):
        """Construct a fake HttpError thrown by the API."""
        response = httplib2.Response({'status': status})
        response.reason = reason
        return errors.HttpError(resp=response, content=b'')

    def test_create_smime_info(self):
        smime_info = smime_snippets.create_smime_info('files/cert.p12')

        self.assertIsNotNone(smime_info)
        self.assertListEqual(list(smime_info.keys()), ['pkcs12'])
        self.assertGreater(len(smime_info['pkcs12']), 0)

    def test_create_smime_info_with_password(self):
        smime_info = smime_snippets.create_smime_info('files/cert.p12', 'password')

        self.assertIsNotNone(smime_info)
        self.assertSetEqual(
            set(smime_info.keys()), set(['pkcs12', 'encryptedKeyPassword']))
        self.assertGreater(len(smime_info['pkcs12']), 0)
        self.assertEqual(smime_info['encryptedKeyPassword'], 'password')

    def test_create_smime_info_file_not_found(self):
        smime_info = smime_snippets.create_smime_info('files/notfound.p12')

        self.mock_insert.assert_not_called()
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertIsNone(smime_info)

    def test_insert_smime_info(self):
        insert_result = self.make_fake_insert_result()
        self.mock_insert.return_value = mock.Mock(
            **{'execute.return_value': insert_result})

        smime_info = smime_snippets.create_smime_info('files/cert.p12')
        result = smime_snippets.insert_smime_info(self.mock_service, self.TEST_USER,
                                                  smime_info)

        self.mock_insert.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER, body=smime_info)
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertEqual(result, insert_result)

    def test_insert_smime_info_error(self):
        fake_error = self.make_http_error(500, 'Fake Error')
        self.mock_insert.side_effect = fake_error

        smime_info = smime_snippets.create_smime_info('files/cert.p12')
        result = smime_snippets.insert_smime_info(
            self.mock_service, self.TEST_USER, smime_info, 'user1alias@example.com')

        self.mock_insert.assert_called_with(
            userId=self.TEST_USER,
            sendAsEmail='user1alias@example.com',
            body=smime_info)
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertIsNone(result)

    def test_insert_cert_from_csv(self):
        self.mock_insert.return_value = mock.Mock(
            **{'execute.return_value': self.make_fake_insert_result()})

        smime_snippets.insert_cert_from_csv(lambda x: self.mock_service,
                                            'files/certs.csv')

        self.assertListEqual(self.mock_insert.call_args_list, [
            mock.call(
                userId='user1@example.com',
                sendAsEmail='user1@example.com',
                body=mock.ANY),
            mock.call(
                userId='user2@example.com',
                sendAsEmail='user2@example.com',
                body=mock.ANY)
        ])
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()

    def test_insert_cert_from_csv_fails(self):
        smime_snippets.insert_cert_from_csv(lambda x: self.mock_service,
                                            'files/notfound.csv')

        self.mock_insert.assert_not_called()
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()

    def test_update_smime_certs_no_certs(self):
        self.mock_list.return_value = mock.Mock(**{'execute.return_value': None})

        default_cert_id = smime_snippets.update_smime_certs(self.mock_service,
                                                            self.TEST_USER)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_insert.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertIsNone(default_cert_id)

    def test_update_smime_certs_no_certs_upload_new_cert(self):
        self.mock_list.return_value = mock.Mock(**{'execute.return_value': None})
        self.mock_insert.return_value = mock.Mock(
            **{'execute.return_value': self.make_fake_insert_result()})

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service, self.TEST_USER, cert_filename='files/cert.p12')

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_insert.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER, body=mock.ANY)
        self.mock_set_default.assert_called_with(
            userId=self.TEST_USER,
            sendAsEmail=self.TEST_USER,
            id='new_certificate_id')

        self.assertEqual(default_cert_id, 'new_certificate_id')

    def test_update_smime_certs_valid_default_cert_no_upload(self):
        expire_dt = datetime.datetime.fromtimestamp(self.CURRENT_TIME)
        fake_list_result = self.make_fake_list_result(is_default=[True])
        self.mock_list.return_value = mock.Mock(
            **{'execute.return_value': fake_list_result})

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service,
            self.TEST_USER,
            cert_filename='files/cert.p12',
            expire_dt=expire_dt)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_insert.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertEqual(default_cert_id, 'existing_certificate_id_0')

    def test_update_smime_certs_expired_default_cert_upload_new_cert(self):
        expire_dt = datetime.datetime.fromtimestamp(self.CURRENT_TIME + 2)
        fake_list_result = self.make_fake_list_result(is_default=[True])
        self.mock_list.return_value = mock.Mock(
            **{'execute.return_value': fake_list_result})
        self.mock_insert.return_value = mock.Mock(
            **{'execute.return_value': self.make_fake_insert_result()})

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service,
            self.TEST_USER,
            cert_filename='files/cert.p12',
            expire_dt=expire_dt)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_insert.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER, body=mock.ANY)
        self.mock_set_default.assert_called_with(
            userId=self.TEST_USER,
            sendAsEmail=self.TEST_USER,
            id='new_certificate_id')

        self.assertEqual(default_cert_id, 'new_certificate_id')

    def test_update_smime_certs_default_cert_expired_other_cert_new_default(self):
        expire_dt = datetime.datetime.fromtimestamp(self.CURRENT_TIME)
        fake_list_result = self.make_fake_list_result(
            is_default=[True, False],
            expiration=[self.CURRENT_TIME - 1, self.CURRENT_TIME + 1])
        self.mock_list.return_value = mock.Mock(
            **{'execute.return_value': fake_list_result})

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service,
            self.TEST_USER,
            cert_filename='files/cert.p12',
            expire_dt=expire_dt)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_set_default.assert_called_with(
            userId=self.TEST_USER,
            sendAsEmail=self.TEST_USER,
            id='existing_certificate_id_1')
        self.mock_insert.assert_not_called()

        self.assertEqual(default_cert_id, 'existing_certificate_id_1')

    def test_update_smime_certs_no_defaults_choose_best_cert_as_new_default(self):
        expire_dt = datetime.datetime.fromtimestamp(self.CURRENT_TIME)
        fake_list_result = self.make_fake_list_result(
            is_default=[False, False, False, False],
            expiration=[
                self.CURRENT_TIME + 2, self.CURRENT_TIME + 1, self.CURRENT_TIME + 4,
                self.CURRENT_TIME + 3
            ])
        self.mock_list.return_value = mock.Mock(
            **{'execute.return_value': fake_list_result})

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service,
            self.TEST_USER,
            cert_filename='files/cert.p12',
            expire_dt=expire_dt)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_set_default.assert_called_with(
            userId=self.TEST_USER,
            sendAsEmail=self.TEST_USER,
            id='existing_certificate_id_2')
        self.mock_insert.assert_not_called()

        self.assertEqual(default_cert_id, 'existing_certificate_id_2')

    def test_update_smime_certs_error(self):
        expire_dt = datetime.datetime.fromtimestamp(self.CURRENT_TIME)
        fake_error = self.make_http_error(500, 'Fake Error')
        self.mock_list.side_effect = fake_error

        default_cert_id = smime_snippets.update_smime_certs(
            self.mock_service,
            self.TEST_USER,
            cert_filename='files/cert.p12',
            expire_dt=expire_dt)

        self.mock_list.assert_called_with(
            userId=self.TEST_USER, sendAsEmail=self.TEST_USER)
        self.mock_insert.assert_not_called()
        self.mock_set_default.assert_not_called()

        self.assertIsNone(default_cert_id)

    def test_update_smime_from_csv(self):
        self.mock_list.return_value = mock.Mock(**{'execute.return_value': None})
        self.mock_insert.return_value = mock.Mock(
            **{'execute.return_value': self.make_fake_insert_result()})

        smime_snippets.update_smime_from_csv(lambda x: self.mock_service,
                                             'files/certs.csv')

        self.assertListEqual(self.mock_list.call_args_list, [
            mock.call(userId='user1@example.com', sendAsEmail='user1@example.com'),
            mock.call(userId='user2@example.com', sendAsEmail='user2@example.com'),
            mock.call(userId='user3@example.com', sendAsEmail='user3@example.com'),
        ])
        self.assertListEqual(self.mock_insert.call_args_list, [
            mock.call(
                userId='user1@example.com',
                sendAsEmail='user1@example.com',
                body=mock.ANY),
            mock.call(
                userId='user2@example.com',
                sendAsEmail='user2@example.com',
                body=mock.ANY),
            mock.call(
                userId='user3@example.com',
                sendAsEmail='user3@example.com',
                body=mock.ANY)
        ])
        self.assertListEqual(self.mock_set_default.call_args_list, [
            mock.call(
                userId='user1@example.com',
                sendAsEmail='user1@example.com',
                id='new_certificate_id'),
            mock.call(
                userId='user2@example.com',
                sendAsEmail='user2@example.com',
                id='new_certificate_id'),
            mock.call(
                userId='user3@example.com',
                sendAsEmail='user3@example.com',
                id='new_certificate_id'),
        ])

    def test_update_smime_from_csv_fails(self):
        smime_snippets.update_smime_from_csv(lambda x: self.mock_service,
                                             'files/notfound.csv')

        self.mock_insert.assert_not_called()
        self.mock_list.assert_not_called()
        self.mock_set_default.assert_not_called()


if __name__ == '__main__':
    unittest.main()
