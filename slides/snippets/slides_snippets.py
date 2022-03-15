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

from __future__ import print_function


class SlidesSnippets(object):
    def __init__(self, service, drive_service, sheets_service, credentials):
        self.service = service
        self.drive_service = drive_service
        self.sheets_service = sheets_service
        self.credentials = credentials

    def create_presentation(self, title):
        slides_service = self.service
        # [START slides_create_presentation]
        body = {
            'title': title
        }
        presentation = slides_service.presentations() \
            .create(body=body).execute()
        print('Created presentation with ID: {0}'.format(
            presentation.get('presentationId')))
        # [END slides_create_presentation]
        return presentation

    def copy_presentation(self, presentation_id, copy_title):
        drive_service = self.drive_service
        # [START slides_copy_presentation]
        body = {
            'name': copy_title
        }
        drive_response = drive_service.files().copy(
            fileId=presentation_id, body=body).execute()
        presentation_copy_id = drive_response.get('id')
        # [END slides_copy_presentation]
        return presentation_copy_id

    def create_slide(self, presentation_id, page_id):
        slides_service = self.service
        # [START slides_create_slide]
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': '1',
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            }
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print('Created slide with ID: {0}'.format(
            create_slide_response.get('objectId')))
        # [END slides_create_slide]
        return response

    def create_textbox_with_text(self, presentation_id, page_id):
        slides_service = self.service
        # [START slides_create_textbox_with_text]
        # Create a new square textbox, using the supplied element ID.
        element_id = 'MyTextBox_01'
        pt350 = {
            'magnitude': 350,
            'unit': 'PT'
        }
        requests = [
            {
                'createShape': {
                    'objectId': element_id,
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': page_id,
                        'size': {
                            'height': pt350,
                            'width': pt350
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 350,
                            'translateY': 100,
                            'unit': 'PT'
                        }
                    }
                }
            },

            # Insert text into the box, using the supplied element ID.
            {
                'insertText': {
                    'objectId': element_id,
                    'insertionIndex': 0,
                    'text': 'New Box Text Inserted!'
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_shape_response = response.get('replies')[0].get('createShape')
        print('Created textbox with ID: {0}'.format(
            create_shape_response.get('objectId')))
        # [END slides_create_textbox_with_text]
        return response

    def create_image(self, presentation_id, page_id):
        slides_service = self.service
        # [START slides_create_image]
        # Create a new image, using the supplied object ID,
        # with content downloaded from IMAGE_URL.
        IMAGE_URL = 'https://picsum.photos/200'
        requests = []
        image_id = 'MyImage_01'
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
        response = slides_service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_image_response = response.get('replies')[0].get('createImage')
        print('Created image with ID: {0}'.format(
            create_image_response.get('objectId')))

        # [END slides_create_image]
        return response

    def text_merging(self, template_presentation_id, data_spreadsheet_id):
        slides_service = self.service
        sheets_service = self.sheets_service
        drive_service = self.drive_service
        responses = []
        # [START slides_text_merging]
        # Use the Sheets API to load data, one record per row.
        data_range_notation = 'Customers!A2:M6'
        sheets_response = sheets_service.spreadsheets().values().get(
            spreadsheetId=data_spreadsheet_id,
            range=data_range_notation).execute()
        values = sheets_response.get('values')

        # For each record, create a new merged presentation.
        for row in values:
            customer_name = row[2]       # name in column 3
            case_description = row[5]    # case description in column 6
            total_portfolio = row[11]    # total portfolio in column 12

            # Duplicate the template presentation using the Drive API.
            copy_title = customer_name + ' presentation'
            body = {
                'name': copy_title
            }
            drive_response = drive_service.files().copy(
                fileId=template_presentation_id, body=body).execute()
            presentation_copy_id = drive_response.get('id')

            # Create the text merge (replaceAllText) requests
            # for this presentation.
            requests = [
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{customer-name}}',
                            'matchCase': True
                        },
                        'replaceText': customer_name
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{case-description}}',
                            'matchCase': True
                        },
                        'replaceText': case_description
                    }
                },
                {
                    'replaceAllText': {
                        'containsText': {
                            'text': '{{total-portfolio}}',
                            'matchCase': True
                        },
                        'replaceText': total_portfolio
                    }
                }
            ]

            # Execute the requests for this presentation.
            body = {
                'requests': requests
            }
            response = slides_service.presentations().batchUpdate(
                presentationId=presentation_copy_id, body=body).execute()
            # [START_EXCLUDE silent]
            responses.append(response)
            # [END_EXCLUDE]
            # Count the total number of replacements made.
            num_replacements = 0
            for reply in response.get('replies'):
                num_replacements += reply.get('replaceAllText') \
                    .get('occurrencesChanged')
            print('Created presentation for %s with ID: %s' %
                  (customer_name, presentation_copy_id))
            print('Replaced %d text instances' % num_replacements)

        # [END slides_text_merging]
        return responses

    def image_merging(self, template_presentation_id,
                      image_url, customer_name):
        slides_service = self.service
        drive_service = self.drive_service
        logo_url = image_url
        customer_graphic_url = image_url

        # [START slides_image_merging]
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
            num_replacements += reply.get('replaceAllShapesWithImage') \
                .get('occurrencesChanged')
        print('Created merged presentation with ID: {0}'
              .format(presentation_copy_id))
        print('Replaced %d shapes with images.' % num_replacements)
        # [END slides_image_merging]
        return response

    def simple_text_replace(self, presentation_id, shape_id, replacement_text):
        slides_service = self.service
        # [START slides_simple_text_replace]
        # Remove existing text in the shape, then insert new text.
        requests = []
        requests.append({
            'deleteText': {
                'objectId': shape_id,
                'textRange': {
                    'type': 'ALL'
                }
            }
        })
        requests.append({
            'insertText': {
                'objectId': shape_id,
                'insertionIndex': 0,
                'text': replacement_text
            }
        })

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print('Replaced text in shape with ID: {0}'.format(shape_id))
        # [END slides_simple_text_replace]
        return response

    def text_style_update(self, presentation_id, shape_id):
        slides_service = self.service
        # [START slides_text_style_update]
        # Update the text style so that the first 5 characters are bolded
        # and italicized, the next 5 are displayed in blue 14 pt Times
        # New Roman font, and the next 5 are hyperlinked.
        requests = [
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 0,
                        'endIndex': 5
                    },
                    'style': {
                        'bold': True,
                        'italic': True
                    },
                    'fields': 'bold,italic'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 5,
                        'endIndex': 10
                    },
                    'style': {
                        'fontFamily': 'Times New Roman',
                        'fontSize': {
                            'magnitude': 14,
                            'unit': 'PT'
                        },
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': 1.0,
                                    'green': 0.0,
                                    'red': 0.0
                                }
                            }
                        }
                    },
                    'fields': 'foregroundColor,fontFamily,fontSize'
                }
            },
            {
                'updateTextStyle': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'FIXED_RANGE',
                        'startIndex': 10,
                        'endIndex': 15
                    },
                    'style': {
                        'link': {
                            'url': 'www.example.com'
                        }
                    },
                    'fields': 'link'
                }
            }
        ]

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print('Updated the text style for shape with ID: {0}'.format(shape_id))
        # [END slides_text_style_update]
        return response

    def create_bulleted_text(self, presentation_id, shape_id):
        slides_service = self.service
        # [START slides_create_bulleted_text]
        # Add arrow-diamond-disc bullets to all text in the shape.
        requests = [
            {
                'createParagraphBullets': {
                    'objectId': shape_id,
                    'textRange': {
                        'type': 'ALL'
                    },
                    'bulletPreset': 'BULLET_ARROW_DIAMOND_DISC'
                }
            }
        ]

        # Execute the requests.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print('Added bullets to text in shape with ID: {0}'.format(shape_id))
        # [END slides_create_bulleted_text]
        return response

    def create_sheets_chart(self, presentation_id, page_id, spreadsheet_id,
                            sheet_chart_id):
        slides_service = self.service
        # [START slides_create_sheets_chart]
        # Embed a Sheets chart (indicated by the spreadsheet_id and
        # sheet_chart_id) onto a page in the presentation.
        # Setting the linking mode as "LINKED" allows the
        # chart to be refreshed if the Sheets version is updated.
        emu4M = {
            'magnitude': 4000000,
            'unit': 'EMU'
        }
        presentation_chart_id = 'MyEmbeddedChart'
        requests = [
            {
                'createSheetsChart': {
                    'objectId': presentation_chart_id,
                    'spreadsheetId': spreadsheet_id,
                    'chartId': sheet_chart_id,
                    'linkingMode': 'LINKED',
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
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print('Added a linked Sheets chart with ID: {0}'.format(
            presentation_chart_id))
        # [END slides_create_sheets_chart]
        return response

    def refresh_sheets_chart(self, presentation_id, presentation_chart_id):
        slides_service = self.service
        # [START slides_refresh_sheets_chart]
        # Refresh an existing linked Sheets chart embedded in a presentation.
        requests = [
            {
                'refreshSheetsChart': {
                    'objectId': presentation_chart_id
                }
            }
        ]

        # Execute the request.
        body = {
            'requests': requests
        }
        response = slides_service.presentations().batchUpdate(
            presentationId=presentation_id, body=body).execute()
        print('Refreshed a linked Sheets chart with ID: {0}'
              .format(presentation_chart_id))
        # [END slides_refresh_sheets_chart]
        return response
