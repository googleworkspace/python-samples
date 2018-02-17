#!/bin/bash
for directory in `find . -mindepth 1 -maxdepth 2 -type d | grep "snippets"`
do
  if [ -f "$directory/test.sh" ]; then
    echo "Running tests for $directory:"
    (cd $directory && ./test.sh)
    echo ""
  fi
done
