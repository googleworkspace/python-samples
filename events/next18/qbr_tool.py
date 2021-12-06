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
"""Tool for generating quarterly business reviews.

Reads from an internal data source, pushes that to Google Sheets, then finally
pushes the data to Google Slides
"""

from __future__ import print_function

import argparse
import re

import customer_data_service
import customer_spreadsheet_reader
import presentation_reader
import presentation_writer
import spreadsheet_writer
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import client
from oauth2client import file as oauth_file
from oauth2client import tools

SCOPES = ['https://www.googleapis.com/auth/drive']
store = oauth_file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)

slides_service = build('slides', 'v1', http=creds.authorize(Http()))
sheets_service = build('sheets', 'v4', http=creds.authorize(Http()))
drive_service = build('drive', 'v3', http=creds.authorize(Http()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'command',
        help='The command to run',
        choices=['create_sheet', 'create_presentations', 'add_customers'])
    parser.add_argument('--spreadsheet_id', help='The spreadsheet to use')
    parser.add_argument(
        '--template_id', help='The presentation to use as a template')
    parser.add_argument(
        '--customer_ids', nargs='+', help='The customers to use')
    args = parser.parse_args()

    if args.command == 'create_sheet':
        create_sheet(args.template_id)
    elif args.command == 'create_presentations':
        create_presentations(args.spreadsheet_id, args.customer_ids)
    elif args.command == 'add_customers':
        add_customers(args.spreadsheet_id, args.customer_ids)


def create_sheet(template_id):
    pres_reader = presentation_reader.PresentationReader(
        slides_service, template_id)
    placeholders = pres_reader.GetAllPlaceholders()
    presentation_title = pres_reader.GetTitle()

    # Create the data manager spreadsheet
    spreadsheet_title = 'Data Sheet - ' + presentation_title
    spreadsheet = spreadsheet_writer.CreateSpreadsheet(
        sheets_service=sheets_service,
        title=spreadsheet_title,
        sheet_titles=['Customer Data'])

    # Get the spreadsheet ID and sheet IDs from the created spreadsheet.
    spreadsheet_id = spreadsheet.get('spreadsheetId')
    sheet_id = spreadsheet.get('sheets')[0].get('properties').get('sheetId')

    # Write the placeholders and metadata to the spreadsheet.
    writer = spreadsheet_writer.SpreadsheetWriter(
        sheets_service, spreadsheet_id)
    writer.PopulateColumn(
        sheet_id=sheet_id,
        column_index=0,
        column_id='placeholders',
        values=placeholders)
    writer.AddTemplateIdToSpreadsheetMetadata(template_id)
    writer.ExecuteBatchUpdate()

    print('Spreadsheet URL: https://docs.google.com/spreadsheets/d/' +
          spreadsheet_id)


def add_customers(spreadsheet_id, customer_ids):
    # Read the placeholders by querying for the developer metadata we added
    # while creating the spreadsheet
    spreadsheet_reader = customer_spreadsheet_reader.CustomerSpreadsheetReader(
        sheets_service, spreadsheet_id)
    spreadsheet_reader.ReadColumnData('placeholders')
    customer_spreadsheet = spreadsheet_reader.ExecuteRead()

    sheet_id = customer_spreadsheet.GetSheetId()
    placeholders = customer_spreadsheet.GetColumnData('placeholders')

    # Process the placeholders into our query properties
    properties = []
    for p in placeholders:
        # Remove any suffix from the property name
        m = re.search(r'{(\w+)(\.\w+)*}', p)
        properties.append(m.group(1))

    data_service = customer_data_service.CustomerDataService()
    writer = spreadsheet_writer.SpreadsheetWriter(
        sheets_service, spreadsheet_id)

    for customer_id in customer_ids:
        # Get the customer data from the internal customer data service
        customer_data = data_service.GetCustomerData(customer_id, properties)

        # Write the customer data to the spreadsheet
        writer.InsertColumn(sheet_id=sheet_id, column_index=1)
        writer.PopulateColumn(
            sheet_id=sheet_id,
            column_index=1,
            column_id=customer_id,
            values=customer_data)

    writer.ExecuteBatchUpdate()


def create_presentations(spreadsheet_id, customer_ids):
    spreadsheet_reader = customer_spreadsheet_reader.CustomerSpreadsheetReader(
        sheets_service, spreadsheet_id)

    spreadsheet_reader.ReadColumnData('placeholders')
    for customer_id in customer_ids:
        spreadsheet_reader.ReadColumnData(customer_id)

    customer_spreadsheet = spreadsheet_reader.ExecuteRead()
    placeholders = customer_spreadsheet.GetColumnData('placeholders')

    # Get the template presentation ID and its title
    template_id = customer_spreadsheet.GetTemplateId()
    pres_reader = presentation_reader.PresentationReader(
        slides_service, template_id)
    title = pres_reader.GetTitle()

    # Generate a presentation for each customer
    for customer_id in customer_ids:
        # Create a copy of the presentation
        new_title = customer_id + ' - ' + title
        presentation_id = drive_service.files().copy(
            fileId=template_id, body={
                'name': new_title
            }).execute().get('id')

        # Replace the placeholders with the customer data in the copy
        data = customer_spreadsheet.GetColumnData(customer_id)
        data_dict = dict(zip(placeholders, data))
        writer = presentation_writer.PresentationWriter(slides_service,
                                                        presentation_id)
        for placeholder, value in data_dict.items():
            if re.findall(r'{(\w+).image}', placeholder):
                writer.ReplaceAllShapesWithImage(placeholder, value)
            else:
                writer.ReplaceAllText(placeholder, value)
            writer.ExecuteBatchUpdate()

        print(customer_id +
              ': https://docs.google.com/presentation/d/' + presentation_id)


if __name__ == '__main__':
    main()
