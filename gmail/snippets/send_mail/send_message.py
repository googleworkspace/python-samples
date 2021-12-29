from __future__ import print_function
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import base64
from email.mime.text import MIMEText

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://mail.google.com/']


# [START gmail_send_message]
def gmailSendMessage():
    """Send an email message.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)

        user_id = 'gduser1@workspacesamples.dev'
        sender_id = 'gduser2@workspacesamples.dev'
        subject = 'sample'
        message_body = 'Hi, this is automated mail.Please do not reply '
        message = create_message(sender=sender_id, to=user_id, subject=subject, message_text=message_body)
        send_message = (service.users().messages().send(userId="me", body=message).execute())

        print('Message Id: %s' % send_message['id'])
        return send_message

    except Exception as error:
        print('An error occurred: %s' % error)


def create_message(sender, to, subject, message_text):
    """Create a message for an email.
       Returns: An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


if __name__ == '__main__':
    gmailSendMessage()
# [END gmail_send_message]

