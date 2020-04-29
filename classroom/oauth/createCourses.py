from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from googleapiclient import errors
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/classroom.courses']

def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('classroom', 'v1', credentials=creds)

    # make course Objects
    courses = ["English", "Math", "Science"]
    courseObjects = []
    for course in courses:
        courseObjects.append({'name': course,'section': '','description': '',
                            'room': '','ownerId': 'me'})

    # create the courses
    print('Create Courses...')
    for courseObject in courseObjects:
        try:
            course = service.courses().create(body=courseObject).execute()
            print('Course Creation Succeeded! id: ' + course['id'])
            
        except errors.HttpError:
            print('Course Creation Failed')

if __name__ == '__main__':
    main()
