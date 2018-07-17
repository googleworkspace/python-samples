# Quarterly business review demo

This sample was created for a talk for Google Cloud NEXT'18 entitled "Building
on the Docs Editors: APIs and Apps Script". It is the implementation of a
commandline tool that:

* Extracts template variables out of a Google Slides template presentation
* Writes those variables to a Google Sheets spreadsheet
* Adds data to the spreadsheet based on those variables from a stub data service
* Generates new Google Slides presentations using the template and the
  spreadsheet data

## Getting started

* Follow the [Sheets API python quickstart](https://developers.google.com/sheets/api/quickstart/python)
  * Make sure to save the client-secrets.json in your working directory
* In the developer project you created, also enable the Google Slides API and
  the Google Drive API
* Run the tool:

<pre>
    // Create the spreadsheet from the Google Slides template
    $ python qbr_tool.py create_sheet --template_id &lt;your template id&gt;

    // Add data from the stub customer service
    $ python qbr_tool.py add_customers \
        --spreadsheet_id &lt;your spreadsheet id&gt; \
        --customer_id jupiter

    // Generate the filled in presentation
    $ python qbr_tool.py create_presentations
         --spreadsheet_id &lt;your spreadsheet id&gt; \
         --customer_id jupiter
</pre>
