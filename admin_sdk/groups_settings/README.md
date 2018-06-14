# Google Admin SDK Groups Settings Python Samples

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
python detect_external_access.py
```

## Restrict External Access

This script restricts external access to domain access for the given group.
It requires the same `client_secret.json` file used by the quickstart.


### Install

```
pip install --upgrade google-api-python-client
```

Follow the [Quickstart instructions](https://developers.google.com/admin-sdk/groups-settings/quickstart/python),
to create an OAuth2 client ID and download the `client_secret.json` file into
this directory.

### Run

```
python restrict_external_access.py
```
