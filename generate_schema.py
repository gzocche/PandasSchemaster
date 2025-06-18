#!/usr/bin/env python3
"""
Command-line interface for PandasSchema Generator.

This script provides a convenient entry point for generating schema classes
from data files using the command line.
"""

from pandasschemaster.schema_generator import main

if __name__ == "__main__":
    exit(main())
