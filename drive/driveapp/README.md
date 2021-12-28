# Quickstart: Run a Drive App in Python

Complete the steps described in the rest of this page, and in about five minutes you'll have a simple Drive app that
uploads a file to Google Drive.

To run a quickstart example you'll need:

* Access to the internet and a web browser, in order to authorize the sample app.
* A Google account with Drive enabled.
* An environment to run programs in your selected language.

## Step 1: Get the sample

Clone the `git` repository at `https://github.com/googledrive/quickstart-python`.

    git clone https://github.com/googledrive/quickstart-python

## Step 2: Install the Google Client Library

To install the Google API Python Client on a system, you should use the `pip` command.

    pip install --upgrade google-api-python-client oauth2client

Alternatively, if you are using `virtualenv`, create the environment and install the client library.

    virtualenv ve
    ./ve/bin/pip install --upgrade google-api-python-client oauth2client

If you need to access the Google API Python Client from a Google App Engine project, you can follow the instructions
[here](https://developers.google.com/api-client-library/python/platforms/google_app_engine).

## Step 3: Run the sample

After you have set up your Google API project, installed the Google API client library, and set up the sample source
code, the sample is ready to run.

    python main.py

Or if using `virtualenv`.

    ./ve/bin/python main.py

When you run the sample from command-line, it provides a link you'll need to visit in order to authorize.

1. Browse to the provided URL in your web browser.
2. If you are not already logged into your Google account, you will be prompted to log in. If you are logged into
   multiple Google accounts, you will be asked to select one account to use for the authorization.
3. Copy the code you're given after browsing to the link, and paste it into the prompt `Enter authorization code:`.
   Click **Enter**.

Note: The authorization flow in this example is greatly simplified for demonstration purposes and should not be used in
web applications. For more information,
see [Authorizing your App with Google Drive](http://developers.google.com/drive/about-auth).

When you finish these steps, the sample prints information about the Google Drive file to the screen. The
file `document.txt` is accessible in Google Drive, and is titled `My New Text Document`.

By editing the sample code to provide paths to new files and new titles, you can run a few more simple upload tests.
When you're ready, you could try running some other Drive API methods such as
[files.list](http://developers.google.com/drive/v2/reference/files/list).
