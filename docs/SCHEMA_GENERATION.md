# Schema Generation - Entity Framework Style

This document explains how to use the Entity Framework-like schema generation feature in PandasSchemaster.

## Overview

The `SchemaGenerator` class provides Entity Framework-like functionality for automatically generating schema classes from data files. Similar to how Entity Framework can generate models from a database, this tool generates PandasSchemaster classes from CSV, Excel, JSON, and other data files.

## Features

- **Automatic Type Inference**: Analyzes data to determine appropriate data types
- **Nullable Detection**: Identifies columns that can contain null values
- **Multiple File Formats**: Supports CSV, Excel, JSON, Parquet, TSV
- **Command Line Interface**: Generate schemas from the command line
- **Programmatic API**: Use in Python code for automation
- **Clean Code Generation**: Produces readable, well-documented schema classes

## Quick Start

### Command Line Usage

```bash
# Generate schema from CSV file
python generate_schema.py data.csv -o my_schema.py -c MyDataSchema

# Generate with custom options
python generate_schema.py data.xlsx --sample-size 1000 --no-nullable -v
```

### Programmatic Usage

```python
from pandasschemaster import SchemaGenerator

# Create generator
generator = SchemaGenerator(infer_nullable=True, sample_size=1000)

# Generate schema from file
schema_code = generator.generate_from_file(
    file_path='my_data.csv',
    output_path='generated_schema.py',
    class_name='MyDataSchema'
)

print(schema_code)
```

## Detailed Examples

### Example 1: Generate from CSV

Given a CSV file `employees.csv`:
```csv
employee_id,first_name,last_name,email,hire_date,salary,department,is_active,bonus
1,John,Doe,john.doe@company.com,2020-01-15,75000.0,Engineering,True,5000.0
2,Jane,Smith,jane.smith@company.com,2019-03-22,82000.0,Marketing,True,
3,Bob,Johnson,bob.johnson@company.com,2021-07-10,68000.0,Engineering,False,0.0
```

Generate the schema:
```bash
python generate_schema.py employees.csv -o employee_schema.py -c EmployeeSchema
```

This generates `employee_schema.py`:
```python
import numpy as np
from pandasschemaster import BaseSchema, SchemaColumn

class EmployeeSchema(BaseSchema):
    """
    Schema class generated from data file.
    Source: employees.csv
    Generated with 9 columns.
    """

    EMPLOYEE_ID = SchemaColumn(
        name='employee_id',
        dtype=np.int64,
        nullable=False,
        description='Column with 3 unique values'
    )

    FIRST_NAME = SchemaColumn(
        name='first_name',
        dtype=np.object_,
        nullable=False,
        description='Column with 3 unique values'
    )

    # ... more columns
```

### Example 2: Using Generated Schema

```python
import pandas as pd
from pandasschemaster import SchemaDataFrame
from employee_schema import EmployeeSchema

# Load data with schema validation
df = SchemaDataFrame(
    pd.read_csv('employees.csv'),
    schema_class=EmployeeSchema,
    validate=True,
    auto_cast=True
)

# Type-safe column access
active_employees = df[df[EmployeeSchema.IS_ACTIVE] == True]
avg_salary = active_employees[EmployeeSchema.SALARY].mean()

print(f"Average salary: ${avg_salary:,.2f}")
```

### Example 3: Batch Processing

```python
from pathlib import Path
from pandasschemaster import SchemaGenerator

def generate_schemas_from_directory(data_dir, output_dir):
    """Generate schemas for all CSV files in a directory."""
    generator = SchemaGenerator()
    
    for csv_file in Path(data_dir).glob("*.csv"):
        class_name = f"{csv_file.stem.title()}Schema"
        output_file = Path(output_dir) / f"{csv_file.stem}_schema.py"
        
        print(f"Generating {class_name} from {csv_file}")
        generator.generate_from_file(
            file_path=str(csv_file),
            output_path=str(output_file),
            class_name=class_name
        )

# Generate schemas for all CSV files
generate_schemas_from_directory("data/", "schemas/")
```

## Configuration Options

### SchemaGenerator Parameters

- `infer_nullable` (bool): Whether to infer nullable columns based on null values (default: True)
- `sample_size` (int): Number of rows to sample for analysis (default: None = all rows)

### File Reading Options

You can pass additional arguments to pandas read functions:

```python
# For CSV files with custom options
generator.generate_from_file(
    'data.csv',
    sep=';',           # Custom separator
    encoding='latin1', # Custom encoding
    skiprows=1,        # Skip header rows
    na_values=['N/A', 'NULL']  # Custom null values
)
```

## Type Inference

The generator uses the following type mapping:

| Pandas/Source Type | NumPy Type | Description |
|-------------------|------------|-------------|
| object (numeric) | np.int64 or np.float64 | Auto-detected numeric |
| object (datetime) | np.datetime64 | Auto-detected dates |
| object (boolean) | np.bool_ | Auto-detected booleans |
| object (string) | np.object_ | Text data |
| int64 | np.int64 | Integer numbers |
| float64 | np.float64 | Floating point numbers |
| bool | np.bool_ | Boolean values |
| datetime64 | np.datetime64 | Date/time values |

## Best Practices

### 1. Sample Large Datasets
For very large files, use sampling to speed up analysis:
```python
generator = SchemaGenerator(sample_size=10000)
```

### 2. Review Generated Schemas
Always review and customize generated schemas:
```python
# Generated schema might need customization
SALARY = SchemaColumn(
    name='salary',
    dtype=np.float64,
    nullable=False,
    validator=lambda x: x > 0,  # Add custom validation
    description='Employee salary (must be positive)'
)
```

### 3. Handle Edge Cases
Consider edge cases in your data:
```python
# For columns that might have mixed types
MIXED_COLUMN = SchemaColumn(
    name='mixed_data',
    dtype=np.object_,
    transformer=lambda x: str(x),  # Convert everything to string
    nullable=True
)
```

### 4. Version Control Schemas
Keep generated schemas in version control:
```bash
# Add to git
git add schemas/
git commit -m "Add generated data schemas"
```

## Command Line Reference

```bash
python generate_schema.py [OPTIONS] INPUT_FILE

Arguments:
  INPUT_FILE          Path to input data file

Options:
  -o, --output PATH   Output file for generated schema
  -c, --class-name    Name for the schema class
  -s, --sample-size   Number of rows to sample
  --no-nullable       Don't infer nullable columns
  -v, --verbose       Enable verbose logging
  -h, --help         Show help message
```

## Integration with IDEs

### VS Code
The generated schemas provide excellent IntelliSense support:
```python
# Get autocomplete for schema columns
df[EmployeeSchema.  # <- IntelliSense shows available columns
```

### Type Hints
Generated schemas work well with type checkers:
```python
def process_employees(df: SchemaDataFrame) -> float:
    # Type checker knows the column exists and type
    return df[EmployeeSchema.SALARY].mean()
```

## Migration from Raw DataFrames

### Before (Raw Pandas)
```python
# Error-prone string-based column access
df = pd.read_csv('data.csv')
salary_avg = df['salary'].mean()  # Typos possible
active = df[df['is_active'] == True]  # No type safety
```

### After (With Generated Schema)
```python
# Type-safe, validated access
df = SchemaDataFrame(
    pd.read_csv('data.csv'),
    schema_class=EmployeeSchema
)
salary_avg = df[EmployeeSchema.SALARY].mean()  # Type-safe
active = df[df[EmployeeSchema.IS_ACTIVE] == True]  # Validated
```

## Troubleshooting

### Common Issues

1. **Unsupported File Format**
   ```
   ValueError: Unsupported file format: .xyz
   ```
   Solution: Use supported formats (CSV, Excel, JSON, Parquet, TSV)

2. **Memory Issues with Large Files**
   ```
   MemoryError: Unable to allocate array
   ```
   Solution: Use sampling
   ```python
   generator = SchemaGenerator(sample_size=10000)
   ```

3. **Import Errors in Generated Code**
   ```
   ImportError: No module named 'pandasschemaster'
   ```
   Solution: Ensure PandasSchemaster is installed and in Python path

### Debug Mode
Enable verbose logging for troubleshooting:
```bash
python generate_schema.py data.csv -v
```

This provides detailed information about type inference and column analysis.

## Advanced Usage

### Custom Type Inference
Extend the generator for custom type handling:
```python
class CustomSchemaGenerator(SchemaGenerator):
    def _infer_object_type(self, series):
        # Custom type inference logic
        if self._looks_like_phone_number(series):
            return np.object_  # Keep as string
        return super()._infer_object_type(series)
```

### Integration with CI/CD
Automate schema generation in build pipelines:
```yaml
# GitHub Actions example
- name: Generate schemas
  run: |
    python generate_schema.py data/input.csv -o schemas/input_schema.py
    git add schemas/
    git commit -m "Update generated schemas" || exit 0
```

This Entity Framework-like approach makes working with structured data much more reliable and maintainable!
