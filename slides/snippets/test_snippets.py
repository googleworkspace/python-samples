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

import unittest
from pprint import pformat

from base_test import BaseTest
from slides_snippets import SlidesSnippets


class SnippetsTest(BaseTest):
    IMAGE_URL = 'https://picsum.photos/200'
    TEMPLATE_PRESENTATION_ID = '1ElmXUX6de-b_OkH2iOK8PKS9FfQeln_Rx0aloIg6Rdc'
    DATA_SPREADSHEET_ID = '17eqFZl_WK4WVixX8PjvjfLD77DraoFwMDXeiHB3dvuM'
    CHART_ID = 1107320627
    CUSTOMER_NAME = 'Fake Customer'

    @classmethod
    def setUpClass(cls):
        super(SnippetsTest, cls).setUpClass()
        cls.snippets = SlidesSnippets(
            cls.service,
            cls.drive_service,
            cls.sheets_service,
            cls.credentials)

    def test_create_presentation(self):
        presentation = self.snippets.create_presentation('Title')
        self.assertIsNotNone(presentation)
        self.delete_file_on_cleanup(presentation.get('presentationId'))

    def test_copy_presentation(self):
        presentation_id = self.create_test_presentation()
        copy_id = self.snippets.copy_presentation(
            presentation_id, 'My Duplicate Presentation')
        self.assertIsNotNone(copy_id)
        self.delete_file_on_cleanup(copy_id)

    def test_create_slide(self):
        presentation_id = self.create_test_presentation()
        self.add_slides(presentation_id, 3)
        page_id = 'my_page_id'
        response = self.snippets.create_slide(presentation_id, page_id)
        self.assertEqual(page_id,
                         response.get('replies')[0].get('createSlide').get('objectId'))

    def test_create_textbox_with_text(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        response = self.snippets.create_textbox_with_text(
            presentation_id, page_id)
        self.assertEqual(2, len(response.get('replies')),
                         msg=pformat(response))
        box_id = response.get('replies')[0].get('createShape').get('objectId')
        self.assertIsNotNone(box_id, msg=pformat(response))

    def test_create_image(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        response = self.snippets.create_image(presentation_id, page_id)
        self.assertEqual(1, len(response.get('replies')),
                         msg=pformat(response))
        image_id = response.get('replies')[0].get(
            'createImage').get('objectId')
        self.assertIsNotNone(image_id, msg=pformat(response))

    def test_text_merging(self):
        responses = self.snippets.text_merging(
            SnippetsTest.TEMPLATE_PRESENTATION_ID,
            SnippetsTest.DATA_SPREADSHEET_ID)
        for response in responses:
            presentation_id = response.get('presentationId')
            self.delete_file_on_cleanup(presentation_id)
            self.assertIsNotNone(presentation_id, msg=pformat(response))
            self.assertEqual(3, len(response.get('replies')),
                             msg=pformat(response))
            num_replacements = 0
            for reply in response.get('replies'):
                num_replacements += reply.get('replaceAllText') \
                    .get('occurrencesChanged')
            self.assertEqual(4, num_replacements, msg=pformat(reply))

    def test_image_merging(self):
        response = self.snippets.image_merging(
            SnippetsTest.TEMPLATE_PRESENTATION_ID,
            SnippetsTest.IMAGE_URL,
            SnippetsTest.CUSTOMER_NAME)
        presentation_id = response.get('presentationId')
        self.delete_file_on_cleanup(presentation_id)
        self.assertIsNotNone(presentation_id, msg=pformat(response))
        self.assertEqual(2, len(response.get('replies')),
                         msg=pformat(response))
        num_replacements = 0
        for reply in response.get('replies'):
            num_replacements += reply.get('replaceAllShapesWithImage') \
                .get('occurrencesChanged')
        self.assertEqual(2, num_replacements)

    def test_simple_text_replace(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        box_id = self.create_test_textbox(presentation_id, page_id)
        response = self.snippets.simple_text_replace(
            presentation_id, box_id, 'MY NEW TEXT')
        self.assertEqual(2, len(response.get('replies')),
                         msg=pformat(response))

    def test_text_style_update(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        box_id = self.create_test_textbox(presentation_id, page_id)
        response = self.snippets.text_style_update(presentation_id, box_id)
        self.assertEqual(3, len(response.get('replies')),
                         msg=pformat(response))

    def test_create_bulleted_text(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        box_id = self.create_test_textbox(presentation_id, page_id)
        response = self.snippets.create_bulleted_text(presentation_id, box_id)
        self.assertEqual(1, len(response.get('replies')),
                         msg=pformat(response))

    def test_create_sheets_chart(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        response = self.snippets.create_sheets_chart(presentation_id,
                                                     page_id, SnippetsTest.DATA_SPREADSHEET_ID, SnippetsTest.CHART_ID)
        self.assertEqual(1, len(response.get('replies')),
                         msg=pformat(response))
        chart_id = response.get('replies')[0].get('createSheetsChart') \
            .get('objectId')
        self.assertIsNotNone(chart_id, msg=pformat(response))

    def test_refresh_sheets_chart(self):
        presentation_id = self.create_test_presentation()
        page_id = self.add_slides(presentation_id, 1, 'BLANK')[0]
        chart_id = self.create_test_sheets_chart(presentation_id,
                                                 page_id, SnippetsTest.DATA_SPREADSHEET_ID, SnippetsTest.CHART_ID)
        response = self.snippets.refresh_sheets_chart(
            presentation_id, chart_id)
        self.assertEqual(1, len(response.get('replies')),
                         msg=pformat(response))


if __name__ == '__main__':
    unittest.main()
