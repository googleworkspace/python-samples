from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/classroom.courses'

def main():
    """Shows basic usage of the Classroom API.
    Prints the names of the first 10 courses the user has access to.
    """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    store = file.Storage('token.json')
    print(store)
    creds = None
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    # [START classroom_quickstart]
    service = build('classroom', 'v1', http=creds.authorize(Http()))

    alias = 'd:school_math_101'
    course = {
        'id': alias,
        'name': 'Math 101',
        'section': 'Period 2',
        'description': 'Course Description',
        'room': '301',
        'ownerId': 'teacherId'
    }
    try:
        course = service.courses().create(
            body=course).execute()
    except:
        print('Course Creation Failed')
        # Handle error
    # [END classroom_quickstart

if __name__ == '__main__':
    main()
