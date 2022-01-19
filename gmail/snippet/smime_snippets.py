"""Snippets for managing S/MIME certificate for a user's account.

These snippets appear at:
https://developers.google.com/gmail/api/guides/smime_certs
"""
import base64
import csv
import datetime

from apiclient import errors


# [START create_smime_info]
def create_smime_info(cert_filename, cert_password=None):
    """Create an smimeInfo resource for a certificate from file.

    Args:
      cert_filename: Name of the file containing the S/MIME certificate.
      cert_password: Password for the certificate file, or None if the file is not
          password-protected.
    """
    smime_info = None
    try:
        with open(cert_filename, 'r') as f:
            smime_info = {}
            data = f.read().encode('UTF-8')
            smime_info['pkcs12'] = base64.urlsafe_b64encode(data)
            if cert_password and len(cert_password) > 0:
                smime_info['encryptedKeyPassword'] = cert_password
    except (OSError, IOError) as error:
        print('An error occurred while reading the certificate file: %s' % error)

    return smime_info


# [END create_smime_info]


# [START insert_smime_info]
def insert_smime_info(service, user_id, smime_info, send_as_email=None):
    """Upload an S/MIME certificate for the user.

    Args:
      service: Authorized GMail API service instance.
      user_id: User's email address.
      smime_info: The smimeInfo resource containing the user's S/MIME certificate.
      send_as_email: The "send as" email address, or None if it should be the same
          as user_id.
    """
    if not send_as_email:
        send_as_email = user_id
    try:
        results = service.users().settings().sendAs().smimeInfo().insert(
            userId=user_id, sendAsEmail=send_as_email, body=smime_info).execute()
        print('Inserted certificate; id: %s' % results['id'])
        return results
    except errors.HttpError as error:
        print('An error occurred: %s' % error)
        return None


# [END insert_smime_info]


# [START insert_cert_from_csv]
def insert_cert_from_csv(service_builder, csv_filename):
    """Upload S/MIME certificates based on the contents of a CSV file.

    Each row of the CSV file should contain a user ID, path to the certificate,
    and the certificate password.

    Args:
      service_builder: A function that returns an authorized GMail API service
          instance for a given user.
      csv_filename: Name of the CSV file.
    """
    try:
        with open(csv_filename, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader, None)  # skip CSV file header
            for row in csv_reader:
                user_id = row[0]
                cert_filename = row[1]
                cert_password = row[2]
                smime_info = create_smime_info(cert_filename, cert_password)
                if smime_info:
                    insert_smime_info(service_builder(user_id), user_id, smime_info)
                else:
                    print('Unable to read certificate file for user_id: %s' % user_id)
    except (OSError, IOError) as error:
        print('An error occured while reading the CSV file: %s' % error)


# [END insert_cert_from_csv]


# [START update_smime_certs]
def update_smime_certs(service,
                       user_id,
                       send_as_email=None,
                       cert_filename=None,
                       cert_password=None,
                       expire_dt=None):
    """Update S/MIME certificates for the user.

    First performs a lookup of all certificates for a user.  If there are no
    certificates, or they all expire before the specified date/time, uploads the
    certificate in the specified file.  If the default certificate is expired or
    there was no default set, chooses the certificate with the expiration furthest
    into the future and sets it as default.

    Args:
      service: Authorized GMail API service instance.
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
    """
    if not send_as_email:
        send_as_email = user_id

    try:
        results = service.users().settings().sendAs().smimeInfo().list(
            userId=user_id, sendAsEmail=send_as_email).execute()
    except errors.HttpError as error:
        print('An error occurred during list: %s' % error)
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
            smime_info = create_smime_info(cert_filename, cert_password)
            results = insert_smime_info(service, user_id, smime_info)
            if results:
                default_id = results['id']

        if default_id:
            try:
                service.users().settings().sendAs().smimeInfo().setDefault(
                    userId=user_id, sendAsEmail=send_as_email, id=default_id).execute()
                return default_id
            except errors.HttpError as error:
                print('An error occurred during setDefault: %s' % error)
    else:
        return default_cert_id

    return None


def update_smime_from_csv(service_builder, csv_filename, expire_dt=None):
    """Update S/MIME certificates based on the contents of a CSV file.

    Each row of the CSV file should contain a user ID, path to the certificate,
    and the certificate password.

    Args:
      service_builder: A function that returns an authorized GMail API service
          instance for a given user.
      csv_filename: Name of the CSV file.
      expire_dt: DateTime object against which the certificate expiration is
        compared.  If None, uses the current time.
    """
    try:
        with open(csv_filename, 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            next(csv_reader, None)  # skip CSV file header
            for row in csv_reader:
                user_id = row[0]
                update_smime_certs(
                    service_builder(user_id),
                    user_id,
                    cert_filename=row[1],
                    cert_password=row[2],
                    expire_dt=expire_dt)
    except (OSError, IOError) as error:
        print('An error occured while reading the CSV file: %s' % error)
# [END update_smime_certs]
