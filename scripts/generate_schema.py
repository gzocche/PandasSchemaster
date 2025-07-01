#!/usr/bin/env python3
"""
Simple command-line script for generating PandasSchemaster classes from data files.

This script provides an easy-to-use interface for the schema generator functionality.
It can read various data formats (CSV, Excel, JSON, Parquet) and generate corresponding
schema classes.

Usage examples:
    python generate_schema.py data.csv
    python generate_schema.py data.csv -o schema.py -c MySchema
    python generate_schema.py data.xlsx --verbose
    python generate_schema.py data.json -s 1000 --no-nullable

Supported file formats:
    - CSV (.csv)
    - Excel (.xlsx, .xls) 
    - JSON (.json)
    - Parquet (.parquet)
    - Tab-separated (.tsv, .txt)

Options:
    -o, --output FILE       Save schema to file (default: print to console)
    -c, --class-name NAME   Custom class name (default: derived from filename)
    -s, --sample-size N     Number of rows to sample (default: use all rows)
    --no-nullable           Don't infer nullable columns
    -v, --verbose           Enable verbose logging
    -h, --help             Show this help message
"""

import sys
import os

# Add the parent directory to Python path to find pandasschemaster package
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    from pandasschemaster.schema_generator import main
    sys.exit(main())
