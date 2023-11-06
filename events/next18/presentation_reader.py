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
"""Reads presentation data.

Retrieves a presentation and extracts the placeholders and the presentation's
title.
"""
import re


class PresentationReader(object):

  def __init__(self, slides_service, presentation_id):
    self._slides_service = slides_service
    self._presentation_id = presentation_id
    self._presentation = None

  def _InitPresentation(self):
    if not self._presentation:
      self._presentation = (
          self._slides_service.presentations()
          .get(presentationId=self._presentation_id)
          .execute()
      )

  def GetTitle(self):
    self._InitPresentation()
    return self._presentation.get("title")

  def GetAllPlaceholders(self):
    self._InitPresentation()
    slides = self._presentation.get("slides")
    placeholders = []
    for slide in slides:
      elements = slide.get("pageElements")
      for element in elements:
        shape = element.get("shape")
        table = element.get("table")
        # Skip page elements that aren't shapes or tables since they're
        # the only types that support text.
        if not shape and not table:
          continue
        if shape:
          placeholders += self._GetPlaceholdersFromText(shape.get("text"))
        elif table:
          rows = table.get("tableRows")
          for row in rows:
            cells = row.get("tableCells")
            for cell in cells:
              placeholders += self._GetPlaceholdersFromText(cell.get("text"))
    # Return the unique placeholders
    seen = set()
    return [p for p in placeholders if not (p in seen or seen.add(p))]

  def _GetPlaceholdersFromText(self, text):
    if not text:
      return []
    placeholders = []
    elements = text.get("textElements")
    for element in elements:
      if element.get("textRun"):
        content = element.get("textRun").get("content")
        placeholders += re.findall("{.*?}", content)
    return placeholders
