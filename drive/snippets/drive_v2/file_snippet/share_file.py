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

# [START drive_share_file]
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def share_file(real_file_id, real_user, real_domain):
  """Batch permission modification.
  Args:
      real_file_id: file Id
      real_user: User ID
      real_domain: Domain of the user ID
  Prints modified permissions

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  creds, _ = google.auth.default()

  try:
    # create drive api client
    service = build("drive", "v2", credentials=creds)
    ids = []
    file_id = real_file_id

    def callback(request_id, response, exception):
      if exception:
        print(exception)
      else:
        print(f"Request_Id: {request_id}")
        print(f'Permission Id: {response.get("id")}')
        ids.append(response.get("id"))

    # pylint: disable=maybe-no-member
    batch = service.new_batch_http_request(callback=callback)
    user_permission = {
        "type": "user",
        "role": "writer",
        "value": "user@example.com",
    }
    user_permission["value"] = real_user
    batch.add(
        service.permissions().insert(
            fileId=file_id,
            body=user_permission,
            fields="id",
        )
    )
    domain_permission = {
        "type": "domain",
        "role": "reader",
        "value": "example.com",
    }
    domain_permission["value"] = real_domain
    batch.add(
        service.permissions().insert(
            fileId=file_id,
            body=domain_permission,
            fields="id",
        )
    )
    batch.execute()

  except HttpError as error:
    print(f"An error occurred: {error}")
    ids = None

  return ids


if __name__ == "__main__":
  share_file(
      real_file_id="1dUiRSoAQKkM3a4nTPeNQWgiuau1KdQ_l",
      real_user="anurag@workspacesamples.dev",
      real_domain="workspacesamples.dev",
  )
# [END drive_share_file]
