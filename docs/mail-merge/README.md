# Mail Merge Sample (Python) for Google Docs (REST) API

## Prerequisites

- Access to the internet and a web browser
- A Google account (G Suite accounts may require administrator approval)
- Basic Python skills (2.x or 3.x)
- Google APIs project with the [Drive](https://developers.google.com/drive/), [Sheets](https://developers.google.com/sheets/), and [Docs](https://developers.google.com/docs/) APIs enabled

## Description

Before getting started, create a new project (or reuse an existing one) at <https://console.developers.google.com> with Google Drive and Docs APIs enabled. (See the videos listed below if you're new to Google APIs.) Then install the Google APIs Client Library for Python if you haven't already: `pip{,3} install -U google-api-python-client`

This sample app requires you to [create a new Google Docs file](https://docs.google.com). Choose whatever template you wish to use, but we suggest using the Letter/Spearmint one to keep things simple. Replace the contact information in the Doc with template variables that we can merge with desired data.

Here is a [sample Letter template](https://drive.google.com/open?id=1Rr7eKm3tvUgRKRoOYVSMF69IVAHIOPS72-l0CzsPmfM) to get an idea of what we mean: ![sample Letter template](https://user-images.githubusercontent.com/1102504/44741564-51ea2480-aab2-11e8-871c-a836626b2a0d.png "sample Letter template")

In the document, the variable names used by the sample app are:

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

After you've templatized the Google Doc, be sure to grab its file ID — in your browser, look at the address bar, and extract the long alphanumeric string that makes up the Drive file ID from the URL: `https://docs.google.com/document/d/<DRIVE_FILE_ID>/edit`.

Replace `YOUR_TMPL_DOC_FILE_ID` in the `docs_mail_merge.py` source file with this file ID as the string value (in quotes) for the `DOCS_FILE_ID` variable. Run the sample app, accept the OAuth2 permissions requested, and when the script has completed, you should have a new mail-merged Google Doc named `Merged form letter` in your Google Drive folder!

## Data source

The application currently supports two different sources of data, plain text and Google Sheets. By default, the sample uses plain text via the `TARGET_TEXT` variable. A better option is to use a Google Sheet. Enable the API for your project in the developers console, and change the `source` variable at the bottom to `'sheets'`. Be sure you create a Sheet which looks like the below and set the `SHEETS_FILE_ID` variable to its file ID.

![sample Sheets data source](https://user-images.githubusercontent.com/1102504/54064578-62e6c180-41ca-11e9-86f6-9d147ac17200.png "sample Sheets data source")

## Testing

The unit-test script is `docs_mail_merge_test.py`; these are the current tests available:

1. Confirm OAuth2 credentials file was downloaded from the API project in the developers console as `credentials.json`.
1. Confirm those OAuth2 credentials can issue requests to Google APIs
1. Confirm project can connect to the Drive, Sheets, and Docs APIs
1. Confirm correct project setup & enabled-APIs by creating & deleting a temp Docs file.
1. Confirm correct project setup & enabled-APIs by copying an existing Docs file then deleting it.
1. Confirm application can retrieve data from plain text source.
1. Confirm application can retrieve data from Google Sheets source.

## Reference

- Google Drive API
    - [API documentation](https://developers.google.com/drive)
    - [Support channels](https://developers.google.com/drive/api/v3/support)
- Google Docs API
    - [API documentation](https://developers.google.com/docs)
    - [Python Quickstart](https://developers.google.com/docs/api/quickstart/python)
    - [Support channels](https://developers.google.com/docs/api/support)
- Google Sheets API
    - [API documentation](https://developers.google.com/sheets)
    - [Support channels](https://developers.google.com/sheets/api/support)
- [Google APIs Client Libraries](https://developers.google.com/api-client-library)
- [G Suite developer overview &amp; video](https://developers.google.com/gsuite)
- [G Suite (REST) APIs intro codelab](https://g.co/codelabs/gsuite-apis-intro) (~half-hour)
- Introductory API videos
    - [New Google APIs project setup](https://goo.gl/RbyTFD) (6:54)
    - [Common Python boilerplate code review](https://goo.gl/KMfbeK) (3:48)
    - [REST APIs intro (Drive API)](https://goo.gl/ZIgf8k) (6:20)
