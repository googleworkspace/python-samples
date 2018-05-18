# Google Admin SDK Groups Settings Python Samples

## Quickstart

Complete the steps described in the [Google Admin SDK Groups Settings Python
Quickstart](https://developers.google.com/admin-sdk/groups-settings/quickstart/python),
and in about five minutes you'll have a simple Python command-line application
that makes requests to the Google Admin SDK Groups Settings API.

### Install

```
pip install --upgrade google-api-python-client
```

### Run

```
python quickstart.py
```

## Detect External Access

This script lists all groups in your domain with some form of external access
enabled. It requires the same `client_secret.json` file used by the quickstart,
but also requires that the Admin SDK be enabled on the Cloud Console project.

### Install

```
pip install --upgrade google-api-python-client
```

Follow the [Quickstart instructions](https://developers.google.com/admin-sdk/groups-settings/quickstart/python),
to create an OAuth2 client ID and download the `client_secret.json` file into
this directory.

### Run

```
detect_external_access.py
```
