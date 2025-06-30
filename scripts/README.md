# PandasSchemaster Generator CLI

A simple command-line tool for generating schema classes from data files.

## Quick Start

The easiest way to use the schema generator is through the `generate_schema.py` script:

```bash
# Basic usage - generate schema and print to console
python generate_schema.py data.csv

# Save schema to a file
python generate_schema.py data.csv -o my_schema.py

# Use a custom class name
python generate_schema.py data.csv -c CustomerSchema

# Sample only first 1000 rows for large files
python generate_schema.py large_data.csv -s 1000

# Enable verbose output
python generate_schema.py data.csv -v

# Disable nullable inference (all columns will be non-nullable)
python generate_schema.py data.csv --no-nullable
```

## Supported File Formats

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **JSON** (`.json`) - JavaScript Object Notation
- **Parquet** (`.parquet`) - Apache Parquet format
- **TSV/TXT** (`.tsv`, `.txt`) - Tab-separated values

## Command-Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `input_file` | Path to data file (required) | `data.csv` |
| `-o, --output` | Output file for schema | `-o schema.py` |
| `-c, --class-name` | Custom class name | `-c CustomerSchema` |
| `-s, --sample-size` | Number of rows to analyze | `-s 1000` |
| `--no-nullable` | Disable nullable inference | `--no-nullable` |
| `-v, --verbose` | Enable detailed logging | `-v` |
| `-h, --help` | Show help message | `-h` |

## Examples

### Basic CSV Processing
```bash
python generate_schema.py customers.csv
```

### Excel File with Custom Output
```bash
python generate_schema.py sales_data.xlsx -o sales_schema.py -c SalesDataSchema
```

### Large File with Sampling
```bash
python generate_schema.py huge_dataset.csv -s 5000 -v -o dataset_schema.py
```

### JSON File Processing
```bash
python generate_schema.py api_response.json -c ApiResponseSchema
```

## Generated Schema Example

When you run the generator on a CSV file like this:

```csv
id,name,age,salary,is_active
1,John,25,50000.0,true
2,Jane,30,60000.0,false
3,Bob,35,70000.0,true
```

It will generate a schema class like:

```python
import numpy as np
from pandasschemaster import BaseSchema, SchemaColumn

class GeneratedSchema(BaseSchema):
    """
    Schema class generated from data file.
    Generated with 5 columns.
    """

    ID = SchemaColumn(
        name='id',
        dtype=np.int64,
        nullable=False,
        description='Column with 3 unique values'
    )

    NAME = SchemaColumn(
        name='name',
        dtype=np.object_,
        nullable=False,
        description='Column with 3 unique values'
    )

    AGE = SchemaColumn(
        name='age',
        dtype=np.int64,
        nullable=False,
        description='Column with 3 unique values'
    )

    SALARY = SchemaColumn(
        name='salary',
        dtype=np.float64,
        nullable=False,
        description='Column with 3 unique values'
    )

    IS_ACTIVE = SchemaColumn(
        name='is_active',
        dtype=np.bool_,
        nullable=False,
        description='Column with 2 unique values'
    )
```

## Tips

1. **Large Files**: Use `-s` option to sample data for faster processing
2. **Custom Names**: Use `-c` to provide meaningful class names
3. **File Output**: Use `-o` to save schemas to files for reuse
4. **Debugging**: Use `-v` for detailed information about the generation process
5. **Type Inference**: The tool automatically detects numeric, boolean, datetime, and string types
