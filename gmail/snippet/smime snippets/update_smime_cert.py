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
# [START gmail_update_smime_certs]

from __future__ import print_function

from datetime import datetime

import create_smime_info
import google.auth
import insert_smime_info
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def update_smime_cert(user_id, send_as_email, cert_filename, cert_password,
                      expire_dt):
    """Update S/MIME certificates for the user.

    First performs a lookup of all certificates for a user.  If there are no
    certificates, or they all expire before the specified date/time, uploads the
    certificate in the specified file.  If the default certificate is expired or
    there was no default set, chooses the certificate with the expiration furthest
    into the future and sets it as default.

    Args:
      user_id: User's email address.
      send_as_email: The "send as" email address, or None if it should be the same
          as user_id.
      cert_filename: Name of the file containing the S/MIME certificate.
      cert_password: Password for the certificate file, or None if the file is not
          password-protected.
      expire_dt: DateTime object against which the certificate expiration is
        compared.  If None, uses the current time.

    Returns:
      The ID of the default certificate.

    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    if not send_as_email:
        send_as_email = user_id

    creds, _ = google.auth.default()

    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)

        # pylint: disable=maybe-no-member
        results = service.users().settings().sendAs().smimeInfo().list(
            userId=user_id, sendAsEmail=send_as_email).execute()

    except HttpError as error:
        print(F'An error occurred during list: {error}')
        return None

    default_cert_id = None
    best_cert_id = (None, datetime.datetime.fromtimestamp(0))

    if not expire_dt:
        expire_dt = datetime.datetime.now()
    if results and 'smimeInfo' in results:
        for smime_info in results['smimeInfo']:
            cert_id = smime_info['id']
            is_default_cert = smime_info['isDefault']
            if is_default_cert:
                default_cert_id = cert_id
            exp = datetime.datetime.fromtimestamp(smime_info['expiration'] / 1000)
            if exp > expire_dt:
                if exp > best_cert_id[1]:
                    best_cert_id = (cert_id, exp)
            else:
                if is_default_cert:
                    default_cert_id = None

    if not default_cert_id:
        default_id = best_cert_id[0]
        if not default_id and cert_filename:
            create_smime_info.create_smime_info(cert_filename=cert_filename,
                                                cert_password=cert_password)
            results = insert_smime_info.insert_smime_info()
            if results:
                default_id = results['id']

        if default_id:
            try:
                # pylint: disable=maybe-no-member
                service.users().settings().sendAs().smimeInfo().setDefault(
                    userId=user_id, sendAsEmail=send_as_email, id=default_id) \
                    .execute()
                return default_id
            except HttpError as error:
                print(F'An error occurred during setDefault: {error}')
    else:
        return default_cert_id

    return None


if __name__ == '__main__':
    update_smime_cert(user_id='xyz', send_as_email=None, cert_filename='xyz',
                      cert_password='xyz', expire_dt=None)
# [END gmail_update_smime_certs]
