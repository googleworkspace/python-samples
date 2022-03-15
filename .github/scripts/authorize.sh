#! /bin/bash

# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Utility for generating credentials used by tests.

# Union of scopes used by samples
SCOPES=(
    "https://www.googleapis.com/auth/drive"
    "https://www.googleapis.com/auth/drive.activity"
    "https://www.googleapis.com/auth/drive.appdata"
    "https://mail.google.com/"
    "https://www.googleapis.com/auth/classroom.courses"
    "https://www.googleapis.com/auth/classroom.announcements"
    "https://www.googleapis.com/auth/classroom.rosters"
    "https://www.googleapis.com/auth/classroom.topics"
    "https://www.googleapis.com/auth/classroom.guardianlinks.students"
    "https://www.googleapis.com/auth/classroom.coursework.students"
)

if [ -z "$CLIENT_ID_FILE" ]; then
    echo "CLIENT_ID_FILE environment not set. Please set and run again."
    exit 1
fi

if [ ! -f "$CLIENT_ID_FILE" ]; then
    echo "$CLIENT_ID_FILE not found."
    exit 1
fi

printf -v EXPANDED_SCOPES '%s,' "${SCOPES[@]}"
gcloud auth application-default login \
  --client-id-file="$CLIENT_ID_FILE" \
  --scopes="${EXPANDED_SCOPES}"

cat "${HOME}/.config/gcloud/application_default_credentials.json"