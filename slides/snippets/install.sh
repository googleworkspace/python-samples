#!/bin/bash
command -v virtualenv >/dev/null 2>&1 || { echo >&2 "virtualenv required, aborting."; exit 1; }
virtualenv "env" &&
source "env/bin/activate" &&
pip install --upgrade google-api-python-client
deactivate
