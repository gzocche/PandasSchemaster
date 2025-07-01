#!/bin/bash
# PandasSchemstart shell wrapper for Unix/Linux/macOS
# This script provides easy access to the unified PandasSchemaster interface

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$SCRIPT_DIR")"

# Add parent directory to Python path and run the unified script
PYTHONPATH="$PARENT_DIR:$PYTHONPATH" python3 "$SCRIPT_DIR/pandaschemstart.py" "$@"

# Check exit code and provide helpful error message if needed
if [ $? -ne 0 ]; then
    echo
    echo "Error: PandasSchemstart failed to run"
    echo "Make sure Python 3 and required packages are installed:"
    echo "  pip3 install -r requirements.txt"
    echo
fi
