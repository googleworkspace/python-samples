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


def create_smime_info(cert_filename, cert_password):
    """Create an smimeInfo resource for a certificate from file.
    Args:
      cert_filename: Name of the file containing the S/MIME certificate.
      cert_password: Password for the certificate file, or None if the file is not
          password-protected.
    Returns : Smime object, including smime information
    """

    smime_info = None
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
    print(create_smime_info(cert_filename='xyz', cert_password='xyz'))
# [END gmail_create_smime_info]
