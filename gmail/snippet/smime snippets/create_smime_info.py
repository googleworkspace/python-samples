"""Copyright 2018 Google LLC
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
# [START gmail_create_smime_info]

from __future__ import print_function

import base64


def create_smime_info():
    """Create an smimeInfo resource for a certificate from file.
    Returns : Smime object, including smime information
    """

    smime_info = None
    cert_password = None
    cert_filename = 'humble_coder.csr'
    try:
        with open(cert_filename, 'rb') as cert:
            smime_info = {}
            data = cert.read().encode('UTF-8')
            smime_info['pkcs12'] = base64.urlsafe_b64encode(data).decode()
            if cert_password and len(cert_password) > 0:
                smime_info['encryptedKeyPassword'] = cert_password

    except (OSError, IOError) as error:
        print(F'An error occurred while reading the certificate file: {error}')
        smime_info = None

    return smime_info


if __name__ == '__main__':
    print(create_smime_info())
# [END gmail_create_smime_info]
