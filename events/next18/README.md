# Quarterly business review demo

This sample was created for a talk for Google Cloud NEXT'18 entitled "Building
on the Docs Editors: APIs and Apps Script". It is the implementation of a
command-line tool that:

* Extracts template variables out of a Google Slides template presentation
* Writes those variables to a Google Sheets spreadsheet
* Adds data to the spreadsheet based on those variables from a stub data service
* Generates new Google Slides presentations using the template and the
  spreadsheet data

## Getting started

* Follow the [Sheets API python quickstart](https://developers.google.com/sheets/api/quickstart/python)
  * Make sure to save the `credentials.json` file in your working directory
* Enable the Google Slides API, Google Drive API and Google Sheets API in your
  developer project
* Run the tool with no arguments to complete the OAuth consent flow:

```bash
python qbr_tool.py
```

* Run the tool:


```bash
# Create the spreadsheet from the Google Slides template.
# For example, 13My9SxkotWssCc2F5yaXp2fzGrzoYV6maytr3qAT9GQ
python qbr_tool.py create_sheet --template_id <your template id>;

# Outputs:
# Spreadsheet URL: https://docs.google.com/spreadsheets/d/<spreadsheet id>

# Add data from the stub customer service
python qbr_tool.py add_customers \
    --spreadsheet_id <spreadsheet id> \
    --customer_id jupiter

# Generate the filled in presentation
python qbr_tool.py create_presentations
    --spreadsheet_id <spreadsheet id> \
    --customer_id jupiter

# Outputs:
# jupiter: https://docs.google.com/presentations/d/<filled in presentation id>
```

