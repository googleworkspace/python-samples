from datetime import datetime, timedelta

from numpy import long


class SettingsSnippets:

    def __init__(self, service):
        self.service = service

    def update_signature(self):
        gmail_service = self.service
        # [START updateSignature]
        primary_alias = None
        aliases = gmail_service.users().settings().sendAs(). \
            list(userId='me').execute()
        for alias in aliases.get('sendAs'):
            if alias.get('isPrimary'):
                primary_alias = alias
                break

        sendAsConfiguration = {
            'signature': 'I heart cats'
        }
        result = gmail_service.users().settings().sendAs(). \
            patch(userId='me',
                  sendAsEmail=primary_alias.get('sendAsEmail'),
                  body=sendAsConfiguration).execute()
        print('Updated signature for: %s' % result.get('displayName'))
        # [END updateSignature]
        return result.get('signature')

    def create_filter(self, real_label_id):
        gmail_service = self.service
        # [START createFilter]
        label_id = 'Label_14'  # ID of user label to add
        # [START_EXCLUDE silent]
        label_id = real_label_id
        # [END_EXCLUDE]
        filter = {
            'criteria': {
                'from': 'cat-enthusiasts@example.com'
            },
            'action': {
                'addLabelIds': [label_id],
                'removeLabelIds': ['INBOX']
            }
        }
        result = gmail_service.users().settings().filters(). \
            create(userId='me', body=filter).execute()
        print('Created filter: %s' % result.get('id'))
        # [END createFilter]
        return result.get('id')

    def enable_forwarding(self, real_forwarding_address):
        gmail_service = self.service
        # [START enableForwarding]
        address = {
            'forwardingEmail': 'user2@example.com'
        }
        # [START_EXCLUDE silent]
        address = {
            'forwardingEmail': real_forwarding_address
        }
        # [END_EXCLUDE]
        result = gmail_service.users().settings().forwardingAddresses(). \
            create(userId='me', body=address).execute()
        if result.get('verificationStatus') == 'accepted':
            body = {
                'emailAddress': result.get('forwardingEmail'),
                'enabled': True,
                'disposition': 'trash'
            }
            result = gmail_service.users().settings(). \
                updateAutoForwarding(userId='me', body=body).execute()
            # [START_EXCLUDE silent]
            return result
            # [END_EXCLUDE]

        # [END enableForwarding]
        return None

    def enable_auto_reply(self):
        gmail_service = self.service
        # [START enableAutoReply]
        epoch = datetime.utcfromtimestamp(0)
        now = datetime.now()
        start_time = (now - epoch).total_seconds() * 1000
        end_time = (now + timedelta(days=7) - epoch).total_seconds() * 1000
        vacation_settings = {
            'enableAutoReply': True,
            'responseBodyHtml': "I'm on vacation and will reply when I'm "
                                "back in the office. Thanks!",
            'restrictToDomain': True,
            'startTime': long(start_time),
            'endTime': long(end_time)
        }
        response = gmail_service.users().settings(). \
            updateVacation(userId='me', body=vacation_settings).execute()
        # [END enableAutoReply]
        return response
