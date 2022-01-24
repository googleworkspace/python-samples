# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START classroom_get_course]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_get_course(course_id):
    """Shows basic usage of the Classroom API.
    Gets the name of courses the user has access to.
    """
    creds, _ = google.auth.default()

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    # Load pre-authorized user credentials from the environment.
    # TODO(developer) - See https://developers.google.com/identity for
    #  guides on implementing OAuth2 for the application.

    # pylint: disable=maybe-no-member

    try:
        service = build('classroom', 'v1', credentials=creds)

        """ Retrieves a classroom course by its id. """
        try:
            course = service.courses().get(id=course_id).execute()
            print('Course "{%s}" found.' % course.get('name'))
            return course
        except HttpError as error:
            print('Course with ID "{%s}" not found.' % course_id)
            # [END classroom_get_course]
            return error
        return course

    except HttpError as error:
        print('An error occurred: %s' % error)
        return error


if __name__ == '__main__':
    # Put the course_id of course whose details need to be fetched
    classroom_get_course(456203257955)

# [END classroom_get_course]
