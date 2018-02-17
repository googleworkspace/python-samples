#!/bin/bash
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/../../application_credentials.json";
source "env/bin/activate" &&
python -m unittest discover
deactivate
