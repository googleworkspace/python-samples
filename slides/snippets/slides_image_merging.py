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

# [START slides_image_merging]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def image_merging(template_presentation_id,
                  image_url, customer_name):
    """image_merging require template_presentation_id,
        image_url and customer_name
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
    creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:

        slides_service = build('slides', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)
        logo_url = image_url

        customer_graphic_url = image_url

        # Duplicate the template presentation using the Drive API.
        copy_title = customer_name + ' presentation'
        drive_response = drive_service.files().copy(
            fileId=template_presentation_id,
            body={'name': copy_title}).execute()
        presentation_copy_id = drive_response.get('id')

        # Create the image merge (replaceAllShapesWithImage) requests.
        requests = []
        requests.append({
            'replaceAllShapesWithImage': {
                'imageUrl': logo_url,
                'replaceMethod': 'CENTER_INSIDE',
                'containsText': {
                    'text': '{{company-logo}}',
                    'matchCase': True
                }
            }
        })
        requests.append({
            'replaceAllShapesWithImage': {
                'imageUrl': customer_graphic_url,
                'replaceMethod': 'CENTER_INSIDE',
                'containsText': {
                    'text': '{{customer-graphic}}',
                    'matchCase': True
                }
            }
        })

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_copy_id, body=body).execute()

        # Count the number of replacements made.
        num_replacements = 0

        for reply in response.get('replies'):
            # add below line

            if reply.get('occurrencesChanged') is not None:
                # end tag
                num_replacements += reply.get('replaceAllShapesWithImage') \
                    .get('occurrencesChanged')

        print(f"Created merged presentation with ID:"
              f"{presentation_copy_id}")
        print(f"Replaced {num_replacements} shapes with images")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print('Images is not merged')
        return error

    return response


if __name__ == '__main__':
    # Put the template_presentation_id, image_url and customer_name

    image_merging("10QnVUx1X2qHsL17WUidGpPh_SQhXYx40CgIxaKk8jU4",
                  'https://www.google.com/images/branding/'
                  'googlelogo/2x/googlelogo_color_272x92dp.png',
                  'Fake Customer')

    # [END slides_image_merging]
