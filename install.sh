#!/bin/bash

for directory in `find . -mindepth 1 -maxdepth 1 -type d`
do
  if [ -f "$directory/install.sh" ]; then
    echo "Installing dependencies for $(basename $directory):"
    (cd $directory && ./install.sh)
    echo ""
  fi
done
