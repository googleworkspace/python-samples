"""Copyright 2022 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License."""

# [START classroom_add_teacher]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_add_teacher(course_id):
    """
    Adds a teacher to a course with specific course_id.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    service = build('classroom', 'v1', credentials=creds)

    teacher_email = 'gduser1@workspacesamples.dev'
    teacher = {
        'userId': teacher_email
    }

    try:
        teachers = service.courses().teachers()
        teacher = teachers.create(courseId=course_id,
                                  body=teacher).execute()
        print('User %s was added as a teacher to the course with ID %s'
              % (teacher.get('profile').get('name').get('fullName'),
                 course_id))
    except HttpError as error:
        print('User "{%s}" is already a member of this course.'
              % teacher_email)
        return error
    return teachers


if __name__ == '__main__':
    # Put the course_id of course for which Teacher needs to be added.
    classroom_add_teacher(453686957652)
# [END classroom_add_teacher]
