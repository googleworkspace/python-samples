"""Copyright 2022 Google LLC

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


import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# [START classroom_add_alias_existing]
def classroom_add_alias_existing(course_id):
    """
        Adds alias to existing course with specific course_id.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    # [START classroom_existing_alias]
    service = build('classroom', 'v1', credentials=creds)
    alias = 'd:school_math_101'
    course_alias = {
            'alias': alias
        }
    try:
        course_alias = service.courses().aliases().create(
            courseId=course_id,
            body=course_alias).execute()
        return course_alias
    except HttpError as error:
        print(f"An error occurred: {error}")
        print('Alias Creation Failed')
    return course_alias
    # [END classroom_existing_alias]


if __name__ == '__main__':
    # Put the course_id of course whose alias needs to be added.
    classroom_add_alias_existing(456058313539)

# [END classroom_existing_alias]
