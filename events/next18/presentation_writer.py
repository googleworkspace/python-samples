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

# pylint: disable=E1102
# python3
"""Functionality for writing to a presentation."""


class PresentationWriter(object):
  """Queues writes for modifying a presentation.

  Call ExecuteBatchUpdate to flush pending writes.
  """

  def __init__(self, slides_service, presentation_id):
    self._slides_service = slides_service
    self._presentation_id = presentation_id
    self._requests = []

  def ReplaceAllText(self, find_text, replace_text):
    request = {
        "replaceAllText": {
            "replaceText": replace_text,
            "containsText": {"text": find_text, "matchCase": True},
        }
    }
    self._requests.append(request)

  def ReplaceAllShapesWithImage(self, find_text, image_url):
    request = {
        "replaceAllShapesWithImage": {
            "imageUrl": image_url,
            "containsText": {"text": find_text, "matchCase": True},
        }
    }
    self._requests.append(request)

  def ExecuteBatchUpdate(self):
    body = {"requests": self._requests}
    self._requests = []
    self._slides_service.presentations().batchUpdate(
        presentationId=self._presentation_id, body=body
    ).execute()
