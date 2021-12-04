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

set -e

export LC_ALL=C.UTF-8
export LANG=C.UTF-8

CL_FILE="${HOME}/changed_files.txt"

if [ -f "${CL_FILE}" ] && ! grep -q .pylintrc "${CL_FILE}"; then
  grep ".py$" "${HOME}/changed_files.txt"| xargs pylint
else
  find . -iname "*.py" -print0 | xargs pylint
fi
