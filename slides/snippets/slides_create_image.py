"""
Copyright 2018 Google LLC

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

# [START slides_create_image]
from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def create_image(presentation_id, page_id):
    creds, _ = google.auth.default()
    try:
        service = build('slides', 'v1', credentials=creds)
        IMAGE_URL = ('https://www.google.com/images/branding/'
                     'googlelogo/2x/googlelogo_color_272x92dp.png')
        requests = []
        image_id = 'MyImage_02'
        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        requests.append({
            'createImage': {
                'objectId': image_id,
                'url': IMAGE_URL,
                'elementProperties': {
                    'pageObjectId': page_id,
                    'size': {
                        'height': emu4M,
                        'width': emu4M
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': 100000,
                        'translateY': 100000,
                        'unit': 'EMU'
                    }
                }
            }
        })

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')
        print('Created image with ID: {0}'.format(
            create_image_response.get('objectId')))



    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Slides not created")
        return error

    return response


if __name__ == '__main__':
    # Put the presentation_id, Page_id of slides whose list needs
    # to be submitted.
    create_image("16eRvJHRrM8Sej5YA0yCHVzQCPLz31-JhbOa4XpP8Yko", "wa1ercf")
    # [END slides_create_image]
