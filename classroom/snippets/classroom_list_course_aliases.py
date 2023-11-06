"""
Copyright 2022 Google LLC

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

# [START classroom_list_course_aliases]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def classroom_list_course_aliases(course_id):
  """
  Prints the list of the aliases of a specified course the user has access to.
  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """

  creds, _ = google.auth.default()
  try:
    service = build("classroom", "v1", credentials=creds)
    course_aliases = []
    page_token = None

    while True:
      response = (
          service.courses()
          .aliases()
          .list(pageToken=page_token, courseId=course_id)
          .execute()
      )
      course_aliases.extend(response.get("aliases", []))
      page_token = response.get("nextPageToken", None)
      if not page_token:
        break

    if not course_aliases:
      print("No course aliases found.")

    print("Course aliases:")
    for course_alias in course_aliases:
      print(f"{course_alias.get('alias')}")
    return course_aliases
  except HttpError as error:
    print(f"An error occurred: {error}")
    return error


if __name__ == "__main__":
  classroom_list_course_aliases("course_id")

# [END classroom_list_course_aliases]
