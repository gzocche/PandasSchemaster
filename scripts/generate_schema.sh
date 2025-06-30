#!/bin/bash
# Simple shell script for Unix/Linux to run the schema generator
# Usage: ./generate_schema.sh input_file [options]
#
# Examples:
#   ./generate_schema.sh data.csv
#   ./generate_schema.sh data.csv -o schema.py -c MySchema

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/generate_schema.py" "$@"

exit_code=$?
if [ $exit_code -ne 0 ]; then
    echo
    echo "Schema generation failed. Check the error messages above."
fi

exit $exit_code
