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
"""Reads the customer data from the template spreadsheet."""

import collections


class CustomerSpreadsheetReader(object):

  def __init__(self, sheets_service, spreadsheet_id):
    self._sheets_service = sheets_service
    self._spreadsheet_id = spreadsheet_id
    self._data_filters = collections.OrderedDict()

  def ReadColumnData(self, column_id):
    data_filter = {
        "developerMetadataLookup": {
            "metadataKey": "column_id",
            "metadataValue": column_id,
        }
    }
    self._data_filters[column_id] = data_filter

  def ExecuteRead(self):
    filters = list(self._data_filters.values())
    get_body = {"dataFilters": filters}
    read_fields = ",".join([
        "sheets.properties.sheetId",
        "sheets.data.rowData.values.formattedValue",
        "developerMetadata.metadataValue",
    ])
    spreadsheet = (
        self._sheets_service.spreadsheets()
        .getByDataFilter(
            spreadsheetId=self._spreadsheet_id,
            body=get_body,
            fields=read_fields,
        )
        .execute()
    )
    customer_spreadsheet = CustomerSpreadsheet(spreadsheet, self._data_filters)
    self._data_filters = collections.OrderedDict()
    return customer_spreadsheet


class CustomerSpreadsheet(object):

  def __init__(self, spreadsheet, data_filters):
    self._spreadsheet = spreadsheet
    self._data_filters = data_filters

  def GetSheetId(self):
    sheet = self._spreadsheet.get("sheets")[0]
    return sheet.get("properties").get("sheetId")

  def GetTemplateId(self):
    metadata = self._spreadsheet.get("developerMetadata")[0]
    return metadata.get("metadataValue")

  def GetColumnData(self, column_id):
    index = list(self._data_filters.keys()).index(column_id)
    data = self._spreadsheet.get("sheets")[0].get("data")[index]
    values = [
        row.get("values")[0].get("formattedValue")
        for row in data.get("rowData")
    ]
    # Remove the first value which is just the label
    return values[1:]
