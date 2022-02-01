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
# [START gmail_update_smime_from_csv]

import csv

import update_smime_cert


def update_smime_from_csv(csv_filename, expire_dt=None):
    """Update S/MIME certificates based on the contents of a CSV file.

    Each row of the CSV file should contain a user ID, path to the certificate,
    and the certificate password.

    Args:
      csv_filename: Name of the CSV file.
      expire_dt: DateTime object against which the certificate expiration is
        compared.  If None, uses the current time.
    """
    try:
        with open(csv_filename, 'rb') as cert:
            csv_reader = csv.reader(cert, delimiter=',')
            next(csv_reader, None)  # skip CSV file header
            for row in csv_reader:
                user_id = row[0]
                update_smime_cert.update_smime_cert(
                    user_id,
                    send_as_email=user_id,
                    cert_filename=row[1],
                    cert_password=row[2],
                    expire_dt=expire_dt)

    except (OSError, IOError) as error:
        print(F'An error occured while reading the CSV file: {error}')


if __name__ == '__main__':
    update_smime_from_csv(csv_filename='xyz')
# [END gmail_update_smime_from_csv]
