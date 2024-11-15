#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "Searching for ${1}"
source $SCRIPT_DIR/env/bin/activate
python3 $SCRIPT_DIR/search.py search "${1}"
reset

