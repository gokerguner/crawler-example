#!/usr/bin/env bash

# This script compiles specific modules and optionally deletes source code."
# Usage: ./module-compiler.sh
# -d    Delete source code

# exit if there is nonzero
set -e

python='python'
if [ "$use_python3" = "1" ]; then
    python='python3'
fi

echo "Compiling Config"
$python -m nuitka --nofollow-imports --module config --include-package=config --output-dir=./src
echo "Done"
echo "Compiling DB"
$python -m nuitka --nofollow-imports --module db --include-package=db --output-dir=./src
echo "Done"
echo "Compilation finished."

if [[ ! $1 == "-d" ]]
then
    [[ "$0" = "$BASH_SOURCE" ]] && exit 1 || return 1 # handle exits from shell or function but don't exit interactive shell
else
    echo "Deleting the source code..."
    rm -r config db
    echo "Done"
fi    
