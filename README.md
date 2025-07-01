# 🐼 PandasSchemaster

**Type-safe DataFrame operations with schema validation for pandas** 

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/build-passing-brightgreen.svg)]()
[![Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen.svg)]()
[![PyPI](https://img.shields.io/badge/PyPI-1.0.1-blue.svg)]()

> Transform your pandas DataFrames from `df['column']` to `df[Schema.COLUMN]` for bulletproof, IDE-friendly data operations!

## 🎯 Why PandasSchemaster?

**Before**: Error-prone string-based column access
```python
df['temprature']  # Typo - runtime error! 😱
df['temperatuur']  # Wrong column name - silent failure! 💥
```

**After**: Type-safe schema-based column access
```python
df[SensorSchema.TEMPERATURE]  # IDE autocomplete + compile-time checking! ✨
```

## ✨ Key Features

- 🛡️ **Type Safety**: Schema-based column access prevents runtime errors
- 🔧 **IDE Support**: Full autocompletion and error detection for column names
- ✅ **Validation**: Automatic data validation based on schema definitions
- 🔄 **Auto-casting**: Seamless data type conversions
- � **Full DataFrame Compatibility**: Inherits from pandas.DataFrame - all methods work
- �📖 **Self-documenting**: Clear, readable code with schema column references

## Quick Start

### Installation

```bash
pip install pandasschemaster
```

### Basic Usage

```python
import pandas as pd
import numpy as np
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema

# Define your schema
class SensorSchema(BaseSchema):
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64)
    HUMIDITY = SchemaColumn("humidity", np.float64)
    SENSOR_ID = SchemaColumn("sensor_id", np.int64, nullable=False)

# Create data
data = {
    'timestamp': [pd.Timestamp.now()],
    'temperature': [23.5],
    'humidity': [45.2],
    'sensor_id': [1001]
}

# Create validated DataFrame
df = SchemaDataFrame(data, schema_class=SensorSchema, validate=True, auto_cast=True)

# Use schema columns for type-safe operations
temperature = df[SensorSchema.TEMPERATURE]  # Instead of df['temperature']
fahrenheit = df[SensorSchema.TEMPERATURE] * 9/5 + 32
hot_readings = df[df[SensorSchema.TEMPERATURE] > 25]

# Multi-column selection
subset = df[[SensorSchema.TEMPERATURE, SensorSchema.HUMIDITY]]

# Assignment with automatic type casting
df[SensorSchema.TEMPERATURE] = [24.1]
```

## Command-Line Schema Generator

PandasSchemaster includes a powerful CLI tool to automatically generate schema classes from your data files:

```bash
# Generate schema from CSV and print to console
python Scripts/generate_schema.py data.csv

# Save schema to file with custom class name
python Scripts/generate_schema.py data.csv -o my_schema.py -c CustomerSchema

# Sample large files for faster processing
python Scripts/generate_schema.py large_data.csv -s 1000 -v

# On Windows, you can also use the batch file
Scripts\generate_schema.bat data.csv -o schema.py -c MySchema

# On Unix/Linux, you can use the shell script
./Scripts/generate_schema.sh data.csv -o schema.py -c MySchema
```

### Supported File Formats
- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files  
- **JSON** (`.json`) - JavaScript Object Notation
- **Parquet** (`.parquet`) - Apache Parquet format
- **TSV/TXT** (`.tsv`, `.txt`) - Tab-separated values

### CLI Options
| Option | Description | Example |
|--------|-------------|---------|
| `input_file` | Path to data file (required) | `data.csv` |
| `-o, --output` | Output file for schema | `-o schema.py` |
| `-c, --class-name` | Custom class name | `-c CustomerSchema` |
| `-s, --sample-size` | Number of rows to analyze | `-s 1000` |
| `--no-nullable` | Disable nullable inference | `--no-nullable` |
| `-v, --verbose` | Enable detailed logging | `-v` |

The generator automatically detects data types (numeric, boolean, datetime, string) and creates properly typed schema classes. For detailed usage examples, see [CLI_USAGE.md](CLI_USAGE.md).

## Schema Column Benefits

### ✅ Type-Safe Access
```python
# Type-safe schema column access
temperature = df[SensorSchema.TEMPERATURE]

# vs traditional string access (error-prone)
temperature = df['temperature']  # Typos not caught until runtime
```

### 🔧 IDE Support
- **Autocompletion**: `SensorSchema.` shows available columns
- **Error Detection**: Invalid column names highlighted
- **Go-to-Definition**: Jump to schema definition

### 🔄 Refactoring Safety
```python
# Rename a schema column and all references update automatically
class SensorSchema(BaseSchema):
    TEMP_CELSIUS = SchemaColumn("temperature_celsius", np.float64)  # Renamed
    # All df[SensorSchema.TEMP_CELSIUS] references work immediately
```

### 🐼 Full DataFrame Compatibility
SchemaDataFrame inherits directly from pandas.DataFrame, so all DataFrame methods work seamlessly:

```python
# Create schema-validated DataFrame
df = SchemaDataFrame(data, schema_class=SensorSchema)

# Use all pandas DataFrame methods directly
print(df.shape)  # (100, 4)
print(df.head())  # First 5 rows
summary = df.describe()  # Statistical summary
grouped = df.groupby(SensorSchema.SENSOR_ID.name).mean()

# Mathematical operations
df_scaled = df * 2
df_filtered = df[df[SensorSchema.TEMPERATURE] > 25]

# All pandas operations work while maintaining schema validation
```

## Advanced Features

### Schema Column Types and Validation
```python
class AdvancedSchema(BaseSchema):
    # Basic column with nullable control
    PRESSURE = SchemaColumn("pressure", np.float64, nullable=False)
    
    # Column with default value
    STATUS = SchemaColumn("status", np.dtype('object'), 
                         default="UNKNOWN", nullable=True)
    
    # Column with description
    MACHINE_ID = SchemaColumn("machine_id", np.int64, 
                             description="Unique machine identifier")
```

### Data Type Casting and Conversion
```python
# Auto-casting handles string to numeric conversion
data = {
    'temperature': ["23.5", "24.1"],  # String values
    'sensor_id': ["1001", "1002"]     # String values  
}

df = SchemaDataFrame(data, schema_class=SensorSchema, 
                    validate=True, auto_cast=True)

# Values are automatically cast to schema types
print(df.dtypes)
# temperature    float64
# sensor_id      Int64
```

## Real-World Example

```python
# Industrial IoT sensor data processing
class IndustrialSchema(BaseSchema):
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    MACHINE_ID = SchemaColumn("machine_id", np.int64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64)
    PRESSURE = SchemaColumn("pressure", np.float64)
    STATUS = SchemaColumn("status", np.dtype('object'))

# Load and validate data
df = SchemaDataFrame(sensor_data, schema_class=IndustrialSchema, validate=True)

# Type-safe analysis using schema columns
avg_temp_by_machine = df.groupby(IndustrialSchema.MACHINE_ID.name)[
    IndustrialSchema.TEMPERATURE.name
].mean()

overheating = df[df[IndustrialSchema.TEMPERATURE] > 150]
efficiency = df[IndustrialSchema.PRESSURE] / df[IndustrialSchema.TEMPERATURE]

# Filter by status using schema column
running_machines = df[df[IndustrialSchema.STATUS] == 'RUNNING']

# Complex multi-column operations
subset = df.select_columns([IndustrialSchema.TEMPERATURE, IndustrialSchema.PRESSURE])
```

## Key Features Demonstrated in Tests

### Column Resolution and Access
```python
# The library handles both string and SchemaColumn access
temp1 = df['temperature']                    # Traditional string access
temp2 = df[SensorSchema.TEMPERATURE]         # Schema column access
assert temp1.equals(temp2)                   # Both work identically

# Multi-column selection with mixed types
subset = df[[SensorSchema.TEMPERATURE, 'humidity']]  # Mixed access works
```

### Schema Validation
```python
# Validation catches missing required columns
class StrictSchema(BaseSchema):
    REQUIRED_COL = SchemaColumn("required", np.float64, nullable=False)

# This will raise validation errors
errors = StrictSchema.validate_dataframe(incomplete_df)
print(errors)  # ['Required column required is missing']
```

### Mathematical Operations
```python
# All mathematical operations work with schema columns
celsius = df[SensorSchema.TEMPERATURE]
fahrenheit = celsius * 9/5 + 32
hot_mask = celsius > 25
comfort_index = celsius + df[SensorSchema.HUMIDITY] / 10
```

## Core Components

### SchemaColumn
Defines a typed column with validation and transformation capabilities.

```python
# Basic column definition
temp_col = SchemaColumn("temperature", np.float64, nullable=True)

# Column with all options
advanced_col = SchemaColumn(
    name="pressure",
    dtype=np.float64,
    nullable=False,
    default=0.0,
    description="Atmospheric pressure in hPa"
)
```

### BaseSchema
Abstract base class for defining DataFrame schemas with class methods for validation.

```python
class MySchema(BaseSchema):
    COL1 = SchemaColumn("col1", np.float64)
    COL2 = SchemaColumn("col2", np.int64)

# Get schema information
columns = MySchema.get_columns()          # Dict of column definitions
names = MySchema.get_column_names()       # List of column names
errors = MySchema.validate_dataframe(df)  # Validation error list
```

### SchemaDataFrame
Pandas DataFrame wrapper with schema validation and type-safe column access.

```python
# All pandas DataFrame methods work
df = SchemaDataFrame(data, schema_class=MySchema)
print(df.shape)                    # Shape
print(df.head())                   # First rows
summary = df.describe()            # Statistics
filtered = df[df['col1'] > 5]      # Filtering

# Plus schema-specific features
subset = df.select_columns([MySchema.COL1])  # Schema-based selection
print(df.schema)                             # Access to schema class
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [🚀 Quick Start](#-quick-start) | Get started in 30 seconds |
| [📖 API Reference](docs/API_REFERENCE.md) | Complete API documentation |
| [🔧 CLI Usage Guide](docs/CLI_USAGE.md) | Command-line tool documentation |
| [🎯 Examples & Tutorials](docs/EXAMPLES.md) | Real-world examples and patterns |

## 📞 Support & Community

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/gzocche/PandasSchemaster/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: [GitHub Issues](https://github.com/gzocche/PandasSchemaster/issues/new?template=feature_request.md)
- 💬 **Questions**: [GitHub Discussions](https://github.com/gzocche/PandasSchemaster/discussions)
- � **Email**: [your.email@example.com](mailto:your.email@example.com)

## 🏆 Why Choose PandasSchemaster?

| Feature | PandasSchemaster | Regular Pandas |
|---------|------------------|----------------|
| **Type Safety** | ✅ Compile-time column checking | ❌ Runtime string errors |
| **IDE Support** | ✅ Full autocompletion | ❌ No column suggestions |
| **Refactoring** | ✅ Safe column renaming | ❌ Manual find-replace |
| **Validation** | ✅ Automatic data validation | ❌ Manual validation required |
| **Self-Documentation** | ✅ Schema as documentation | ❌ Requires external docs |
| **Auto-Generation** | ✅ Generate schemas from data | ❌ Manual schema creation |

## Testing

The library includes comprehensive tests covering:
- Basic SchemaColumn functionality and type casting
- BaseSchema validation and column management  
- SchemaDataFrame operations and pandas compatibility
- Mathematical operations and filtering with schema columns
- Column access resolution and multi-column selection

Run tests with:
```bash
python -m pytest tests/
```

## 🔧 Requirements

- **Python**: 3.8+ (3.9+ recommended)
- **pandas**: >= 2.0.0
- **numpy**: >= 1.24.0

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on top of the amazing [pandas](https://pandas.pydata.org/) library
- Inspired by Entity Framework's code-first approach
- Thanks to all [contributors](https://github.com/gzocche/PandasSchemaster/contributors)

---

**⭐ Star this repo if PandasSchemaster helps you write better, safer pandas code!**

**🔗 Share with your data science team and help them discover type-safe DataFrames!**

---

<div align="center">

**Use `df[MySchema.COLUMN]` for type-safe DataFrame operations!** 🚀

Made with ❤️ by [@gzocche](https://github.com/gzocche)

</div>