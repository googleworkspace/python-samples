# Mail Merge Sample (Python) for Google Docs (REST) API

## Prerequisites

- Access to the internet and a web browser
- A Google or Gmail account (G Suite accounts may require administrator approval)
- Basic Python skills (2.x or 3.x)
- Google APIs project with the [Drive](https://developers.google.com/drive/)
  , [Sheets](https://developers.google.com/sheets/), and [Docs](https://developers.google.com/docs/) APIs enabled

## Description

Create a new project (or reuse an existing one) from [your developer console](https://console.developers.google.com)
with the three Google APIs above enabled. (See the videos listed at the bottom if you're new to Google APIs.) Ensure you
have the Google APIs Client Library for Python installed; the fastest way of doing this is to
use `pip install -U google-api-python-client` (or with `pip3` if you have both Python 2 and 3 on your computer).

This sample app requires you to [create a new Google Docs file](https://docs.google.com) to serve as the letter template
with variable placeholders. Choose the template you wish to use, but we recommend *Letter/Spearmint* to keep things
simple. Replace the contact information in the Doc with template variables that we can merge with desired data. Here are
the variables we're using:

### General

* `{{DATE}}` — letter to be dated with this date
* `{{BODY}}` — letter content

### Sender

* `{{MY_NAME}}` — sender's name
* `{{MY_ADDRESS}}` — sender's address
* `{{MY_EMAIL}}` — sender's email
* `{{MY_PHONE}}` — sender's telephone number

### Recipient

* `{{TO_NAME}}` — recipient's name
* `{{TO_TITLE}}` — recipient's job title
* `{{TO_COMPANY}}` — recipient's organization
* `{{TO_ADDRESS}}` — recipient's address

Here's one [sample letter template](https://drive.google.com/open?id=1Xycxuuv7OhEQUuzbt_Mw0TPMq02MseSD1vZdBJ3nLjk) to
get an idea of what we mean:

![sample letter template](https://user-images.githubusercontent.com/1102504/54470461-6b5c7080-4765-11e9-9912-01b44c734118.png "sample letter template")

Once you're done, grab your template's file ID — go to the URL in the address bar of your browser and extract the long
alphanumeric string representing the Drive file ID: `https://docs.google.com/document/d/DRIVE_FILE_ID/edit`.
Replace `YOUR_TMPL_DOC_FILE_ID` with this ID as the `DOCS_FILE_ID` string variable (keep in quotes).

## Data source

Next, decide on the data source. This sample app currently supports plain text and Google Sheets. By default,
the `TARGET_TEXT` variable is set to `'text'` but change to `'sheets'` once you have a Google Sheet with the data. The
code supports a Sheet structured like this:

![sample Sheets data source](https://user-images.githubusercontent.com/1102504/54470464-731c1500-4765-11e9-9110-986519502cdf.png "sample Sheets data source")

Here is [one example Sheet](https://drive.google.com/open?id=18yqXLEMx6l__VAIN-Zo52pL18F3rXn0_-K6gZ-vwPcc) you can model
yours with. Ensure you then set the `SHEETS_FILE_ID` variable to its file ID (get it the same way as your Google Doc).

## Application code

The application script (`docs_mail_merge.py`) supplies a data structure (`merge`) with the sender info, date, body of
the letter, and placeholders for values that will be replaced by data from the selected data source. The data is fetched
and merged into form letters in a loop, displaying links to each of the merged letters. One function is used to fetch
the data, supported by private function "shims" for each data source. The other pair of functions: a private function to
copy the template, and one more for merging the form data into a copy of the template.

If you run the sample app as written (with all real variables and data documents) and accept the OAuth2 permissions.
You'll see one line of output per letter merged. Those letters, named `Merged form letter`, will also be found in your
Google Drive. If you run the app with our data featured here, your merged letter should look like this:

![sample merged letter](https://user-images.githubusercontent.com/1102504/54470465-731c1500-4765-11e9-8a0a-93a3bb445d6e.png "sample merged letter")

## Testing

The unit-test script is `docs_mail_merge_test.py`; see the file for a list of the available tests.

## Reference

- Google Drive API
  - [API documentation](https://developers.google.com/drive/)
  - [Support channels](https://developers.google.com/drive/api/v3/support/)
- Google Docs API
  - [API documentation](https://developers.google.com/docs/)
  - [Support channels](https://developers.google.com/docs/api/support/)
- Google Sheets API
  - [API documentation](https://developers.google.com/sheets/)
  - [Support channels](https://developers.google.com/sheets/api/support/)
- G Suite APIs
  - [G Suite developer overview &amp; video](https://developers.google.com/gsuite/)
  - [G Suite (REST) APIs intro codelab](https://g.co/codelabs/gsuite-apis-intro/) (30 mins)
  - [Google APIs client libraries](https://developers.google.com/api-client-library/)
- Introductory videos
  - [New Google APIs project setup](https://goo.gl/RbyTFD) (6:54)
  - [Common OAuth2 boilerplate code (Python)](https://goo.gl/KMfbeK) (3:48)
  - [REST APIs intro (Drive API)](https://goo.gl/ZIgf8k) (6:20)
  - [Introducing the Docs API](https://youtu.be/jeU-tWKeb6g) (2:57)

## Enhancements

Here are some recommendations on how you can enhance this application:

1. Adapt this sample for your mail merge use case
1. Support exporting merged letters as PDF (HINT: Drive API)
1. Support importing data from other data sources, i.e., [Cloud SQL](https://cloud.google.com/sql/), Salesforce, etc.
1. Augment the plain text data support to include processing data from CSV files
