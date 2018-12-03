from __future__ import print_function
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive.activity.readonly'


def main():
  """Shows basic usage of the Drive Activity API.
    Prints information about the last 10 events that occured the user's Drive.
    """
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  store = file.Storage('token.json')
  creds = store.get()
  if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
  service = build('driveactivity', 'v2', http=creds.authorize(Http()))

  # Call the Drive Activity API
  results = service.activity().query(body={
      'pageSize': 10,
      'consolidationStrategy': {
          'legacy': {}
      }
  }).execute()
  activities = results.get('activities', [])

  if not activities:
    print('No activity.')
  else:
    print('Recent activity:')
    for activity in activities:
      time = getTimeInfo(activity)
      action = getActionInfo(activity['primaryActionDetail'])
      actors = map(getActorInfo, activity['actors'])
      targets = map(getTargetInfo, activity['targets'])
      print(u'{0}: {1}, {2}, {3}'.format(time, truncated(actors), action,
                                         truncated(targets)))


def truncated(array, limit=2):
  contents = ', '.join(array[:limit])
  more = '' if len(array) <= limit else ', ...'
  return '[' + contents + more + ']'


def getTimeInfo(activity):
  if 'timestamp' in activity:
    return activity['timestamp']
  if 'timeRange' in activity:
    return activity['timeRange']['endTime']
  return 'unknown'


def getActionInfo(actionDetail):
  return next(iter(actionDetail))


def getUserInfo(user):
  if 'knownUser' in user:
    knownUser = user['knownUser']
    isMe = knownUser.get('isCurrentUser', False)
    return u'people/me' if isMe else knownUser['personName']
  return next(iter(user))


def getActorInfo(actor):
  if 'user' in actor:
    return getUserInfo(actor['user'])
  return next(iter(actor))


def getTargetInfo(target):
  if 'driveItem' in target:
    return 'driveItem:"' + target['driveItem'].get('title', 'unknown') + '"'
  if 'teamDrive' in target:
    return 'teamDrive:"' + target['teamDrive'].get('title', 'unknown') + '"'
  if 'fileComment' in target:
    parent = target['fileComment'].get('parent', {})
    return 'fileComment:"' + parent.get('title', 'unknown') + '"'
  return next(iter(target))


if __name__ == '__main__':
  main()
