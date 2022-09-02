# Drive V3 Python Quickstart

Complete the steps described in the [Drive V3 Python Quickstart](
https://developers.google.com/drive/v3/web/quickstart/python), and in
about five minutes you'll have a simple Python command-line application that
makes requests to the Drive V3 API.

## Prerequisites
- Python
- Visual Studio Code or another text editor
- An active Google account with access to Google Devlopers

## Getting Started
1. Clone the Github repo either using the git command or by downloading and extracting the folder.
```shell
gh repo clone googleworkspace/python-samples
```
2. Open the extrancted or cloned folder in Visual Studio Code or your text editor.
3. Activate the Drive API in the Google API Console ([Instructions here.](https://developers.google.com/workspace/guides/create-project))
4. Create a OAuth client ID credential and download the OAuth client ID json file ([Instructions here.](https://developers.google.com/workspace/guides/create-credentials))
5. Move the json file into the quickstart folder (*/python-samples/drive/quickstart) and rename it credentials.json

## Install

```shell
pip install -r requirements.txt
```

## Run

```shell
python quickstart.py
```

## Expanding
The Google Drive devloper api can be found [here](https://developers.google.com/drive/api).
