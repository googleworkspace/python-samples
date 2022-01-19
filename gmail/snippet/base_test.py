import os
import unittest

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


class BaseTest(unittest.TestCase):

    RECIPIENT = 'gdtest2@appsrocks.com'
    TEST_USER = 'gdtest1@appsrocks.com'
    FORWARDING_ADDRESS = 'gdtest2@appsrocks.com'

    @classmethod
    def setUpClass(cls):
        cls.service = cls.create_service()

    @classmethod
    def create_credentials(cls):
        scope = ['https://www.googleapis.com/auth/gmail.compose',
                 'https://www.googleapis.com/auth/gmail.send',
                 'https://www.googleapis.com/auth/gmail.labels',
                 'https://www.googleapis.com/auth/gmail.settings.basic',
                 'https://www.googleapis.com/auth/gmail.settings.sharing']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(os.environ['GOOGLE_APPLICATION_CREDENTIALS'],
                                                                       scopes=scope)
        return credentials.create_delegated(BaseTest.TEST_USER)

    @classmethod
    def create_service(cls):
        credentials = cls.create_credentials()
        return discovery.build('gmail', 'v1', credentials=credentials)


if __name__ == '__main__':
    unittest.main()
