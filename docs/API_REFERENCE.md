# 📖 API Reference

Complete API documentation for PandasSchemaster.

## 📋 Table of Contents

- [SchemaColumn](#schemacolumn)
- [BaseSchema](#baseschema)
- [SchemaDataFrame](#schemadataframe)
- [SchemaGenerator](#schemagenerator)

---

## SchemaColumn

The `SchemaColumn` class defines a typed column with validation and transformation capabilities.

### Constructor

```python
SchemaColumn(
    name: str,
    dtype: np.dtype,
    nullable: bool = True,
    default: Any = None,
    description: str = None
)
```

#### Parameters

- **`name`** (`str`): The column name in the DataFrame
- **`dtype`** (`np.dtype`): NumPy data type for the column
- **`nullable`** (`bool`, optional): Whether the column can contain null values. Default: `True`
- **`default`** (`Any`, optional): Default value for missing data. Default: `None`
- **`description`** (`str`, optional): Human-readable description of the column. Default: `None`

#### Examples

```python
import numpy as np
from pandasschemaster import SchemaColumn

# Basic column
temperature = SchemaColumn("temperature", np.float64)

# Non-nullable column with default
sensor_id = SchemaColumn("sensor_id", np.int64, nullable=False, default=0)

# Column with description
timestamp = SchemaColumn(
    "timestamp", 
    np.datetime64, 
    nullable=False,
    description="Sensor reading timestamp"
)
```

### Properties

- **`name`** (`str`): Column name
- **`dtype`** (`np.dtype`): Column data type
- **`nullable`** (`bool`): Whether column accepts null values
- **`default`** (`Any`): Default value
- **`description`** (`str`): Column description

### Methods

#### `validate(data: Any) -> bool`

Validates data against the column definition.

```python
column = SchemaColumn("temp", np.float64)
is_valid = column.validate([23.5, 24.1, 25.0])  # Returns True
```

#### `cast(data: Any) -> Any`

Casts data to the column's data type.

```python
column = SchemaColumn("temp", np.float64)
casted = column.cast(["23.5", "24.1"])  # Returns [23.5, 24.1]
```

---

## BaseSchema

Abstract base class for defining DataFrame schemas with validation methods.

### Usage

```python
from pandasschemaster import BaseSchema, SchemaColumn
import numpy as np

class SensorSchema(BaseSchema):
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64)
    HUMIDITY = SchemaColumn("humidity", np.float64)
    SENSOR_ID = SchemaColumn("sensor_id", np.int64, nullable=False)
```

### Class Methods

#### `get_columns() -> Dict[str, SchemaColumn]`

Returns a dictionary of all schema columns.

```python
columns = SensorSchema.get_columns()
# Returns: {'TIMESTAMP': SchemaColumn(...), 'TEMPERATURE': SchemaColumn(...), ...}
```

#### `get_column_names() -> List[str]`

Returns a list of column names in the DataFrame.

```python
names = SensorSchema.get_column_names()
# Returns: ['timestamp', 'temperature', 'humidity', 'sensor_id']
```

#### `validate_dataframe(df: pd.DataFrame) -> List[str]`

Validates a DataFrame against the schema and returns validation errors.

```python
errors = SensorSchema.validate_dataframe(df)
if errors:
    print(f"Validation failed: {errors}")
else:
    print("DataFrame is valid!")
```

#### `get_schema_info() -> Dict[str, Any]`

Returns comprehensive schema information.

```python
info = SensorSchema.get_schema_info()
# Returns: {
#     'columns': {...},
#     'column_names': [...],
#     'required_columns': [...],
#     'optional_columns': [...]
# }
```

---

## SchemaDataFrame

A pandas DataFrame wrapper with schema validation and type-safe column access.

### Constructor

```python
SchemaDataFrame(
    data: Any,
    schema_class: Type[BaseSchema],
    validate: bool = True,
    auto_cast: bool = True,
    **kwargs
)
```

#### Parameters

- **`data`** (`Any`): Data to create DataFrame from (dict, list, DataFrame, etc.)
- **`schema_class`** (`Type[BaseSchema]`): Schema class defining the structure
- **`validate`** (`bool`, optional): Whether to validate data against schema. Default: `True`
- **`auto_cast`** (`bool`, optional): Whether to automatically cast data types. Default: `True`
- **`**kwargs`**: Additional arguments passed to `pd.DataFrame`

#### Examples

```python
import pandas as pd
from pandasschemaster import SchemaDataFrame

# Create with validation
df = SchemaDataFrame(
    data={'temperature': [23.5, 24.1], 'humidity': [45.2, 46.8]},
    schema_class=SensorSchema,
    validate=True,
    auto_cast=True
)

# Create from existing DataFrame
existing_df = pd.DataFrame(data)
df = SchemaDataFrame(existing_df, SensorSchema)
```

### Properties

- **`schema`** (`Type[BaseSchema]`): The schema class used for validation
- **`df`** (`pd.DataFrame`): The underlying pandas DataFrame

### Methods

#### Column Access

```python
# Type-safe column access
temperature = df[SensorSchema.TEMPERATURE]

# Multi-column selection
subset = df[[SensorSchema.TEMPERATURE, SensorSchema.HUMIDITY]]

# Mixed access (schema + string)
mixed = df[[SensorSchema.TEMPERATURE, 'humidity']]
```

#### `select_columns(columns: List[SchemaColumn]) -> pd.DataFrame`

Select columns using schema column objects.

```python
subset = df.select_columns([SensorSchema.TEMPERATURE, SensorSchema.HUMIDITY])
```

#### `validate_against_schema() -> List[str]`

Validate the current DataFrame against its schema.

```python
errors = df.validate_against_schema()
if errors:
    print(f"Validation errors: {errors}")
```

#### `recast_columns() -> None`

Recast all columns to their schema-defined types.

```python
df.recast_columns()  # Ensures all columns match schema types
```

### Inherited DataFrame Methods

`SchemaDataFrame` inherits from `pd.DataFrame`, so all pandas methods work:

```python
# All pandas operations work
print(df.shape)              # Shape
print(df.head())             # First 5 rows
summary = df.describe()      # Statistical summary
grouped = df.groupby('sensor_id').mean()

# Mathematical operations
df_scaled = df * 2
df_filtered = df[df[SensorSchema.TEMPERATURE] > 25]
```

---

## SchemaGenerator

Generates schema classes from data files, similar to Entity Framework's database-first approach.

### Constructor

```python
SchemaGenerator(
    infer_nullable: bool = True,
    sample_size: Optional[int] = None
)
```

#### Parameters

- **`infer_nullable`** (`bool`, optional): Whether to infer nullable fields. Default: `True`
- **`sample_size`** (`Optional[int]`, optional): Number of rows to sample for type inference. Default: `None` (use all rows)

### Methods

#### `generate_schema_from_file(file_path: str, class_name: str = None) -> str`

Generate a schema class from a data file.

```python
from pandasschemaster import SchemaGenerator

generator = SchemaGenerator()
schema_code = generator.generate_schema_from_file(
    "data.csv", 
    class_name="DataSchema"
)
print(schema_code)
```

#### `generate_schema_from_dataframe(df: pd.DataFrame, class_name: str = "GeneratedSchema") -> str`

Generate a schema class from an existing DataFrame.

```python
import pandas as pd

df = pd.read_csv("data.csv")
generator = SchemaGenerator()
schema_code = generator.generate_schema_from_dataframe(df, "MySchema")
```

#### `infer_column_type(series: pd.Series) -> np.dtype`

Infer the appropriate NumPy dtype for a pandas Series.

```python
import pandas as pd

series = pd.Series([1, 2, 3, 4])
generator = SchemaGenerator()
dtype = generator.infer_column_type(series)  # Returns np.int64
```

#### `is_nullable(series: pd.Series) -> bool`

Determine if a column should be nullable based on its data.

```python
series_with_nulls = pd.Series([1, 2, None, 4])
generator = SchemaGenerator()
nullable = generator.is_nullable(series_with_nulls)  # Returns True
```

### Supported File Formats

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **JSON** (`.json`) - JavaScript Object Notation
- **Parquet** (`.parquet`) - Apache Parquet format
- **TSV/TXT** (`.tsv`, `.txt`) - Tab-separated values

### Example Generated Schema

```python
# Input: CSV file with columns: id, name, temperature, active, created_at
# Generated output:

import numpy as np
from pandasschemaster import BaseSchema, SchemaColumn

class DataSchema(BaseSchema):
    """Auto-generated schema from data.csv"""
    
    ID = SchemaColumn("id", np.int64, nullable=False)
    NAME = SchemaColumn("name", np.object_, nullable=True)
    TEMPERATURE = SchemaColumn("temperature", np.float64, nullable=True)
    ACTIVE = SchemaColumn("active", np.bool_, nullable=True)
    CREATED_AT = SchemaColumn("created_at", np.datetime64, nullable=True)
```

---

## 🎯 Type Mapping Reference

### Pandas to NumPy Type Mapping

| Pandas Type | NumPy Type | Schema Column Example |
|-------------|------------|----------------------|
| `object` | `np.object_` | `SchemaColumn("name", np.object_)` |
| `int64` | `np.int64` | `SchemaColumn("id", np.int64)` |
| `float64` | `np.float64` | `SchemaColumn("price", np.float64)` |
| `bool` | `np.bool_` | `SchemaColumn("active", np.bool_)` |
| `datetime64[ns]` | `np.datetime64` | `SchemaColumn("created", np.datetime64)` |
| `timedelta64[ns]` | `np.timedelta64` | `SchemaColumn("duration", np.timedelta64)` |
| `category` | `np.object_` | `SchemaColumn("category", np.object_)` |

### Common Usage Patterns

#### Financial Data Schema
```python
class FinancialSchema(BaseSchema):
    SYMBOL = SchemaColumn("symbol", np.object_, nullable=False)
    PRICE = SchemaColumn("price", np.float64, nullable=False)
    VOLUME = SchemaColumn("volume", np.int64, nullable=False)
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    CHANGE_PCT = SchemaColumn("change_pct", np.float64, nullable=True)
```

#### IoT Sensor Schema
```python
class IoTSchema(BaseSchema):
    DEVICE_ID = SchemaColumn("device_id", np.object_, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64, nullable=True)
    HUMIDITY = SchemaColumn("humidity", np.float64, nullable=True)
    BATTERY_LEVEL = SchemaColumn("battery_level", np.int64, nullable=True)
    LAST_SEEN = SchemaColumn("last_seen", np.datetime64, nullable=False)
    IS_ACTIVE = SchemaColumn("is_active", np.bool_, nullable=False, default=True)
```

#### User Analytics Schema
```python
class UserAnalyticsSchema(BaseSchema):
    USER_ID = SchemaColumn("user_id", np.int64, nullable=False)
    SESSION_ID = SchemaColumn("session_id", np.object_, nullable=False)
    PAGE_VIEWS = SchemaColumn("page_views", np.int64, nullable=False, default=0)
    SESSION_DURATION = SchemaColumn("session_duration", np.timedelta64, nullable=True)
    CONVERSION = SchemaColumn("conversion", np.bool_, nullable=False, default=False)
    REVENUE = SchemaColumn("revenue", np.float64, nullable=True, default=0.0)
```

---

## 🔧 Error Handling

### Common Validation Errors

#### Missing Required Columns
```python
# Error: Required column 'sensor_id' is missing
errors = SensorSchema.validate_dataframe(df)
# Returns: ['Required column sensor_id is missing']
```

#### Type Mismatch
```python
# Error: Column contains invalid data type
column = SchemaColumn("temperature", np.float64)
result = column.validate(["not", "a", "number"])  # Returns False
```

#### Nullable Constraint Violation
```python
# Error: Non-nullable column contains null values
column = SchemaColumn("id", np.int64, nullable=False)
result = column.validate([1, 2, None, 4])  # Returns False
```

### Best Practices for Error Handling

```python
# Always check validation results
df = SchemaDataFrame(data, SensorSchema, validate=True)
errors = df.validate_against_schema()

if errors:
    print("Validation failed:")
    for error in errors:
        print(f"  - {error}")
    # Handle errors appropriately
else:
    print("Data is valid!")
    # Proceed with processing
```

---

## 🚀 Performance Tips

### Large DataFrames
```python
# Use sampling for large files
generator = SchemaGenerator(sample_size=10000)
schema = generator.generate_schema_from_file("huge_file.csv")

# Disable validation for better performance
df = SchemaDataFrame(data, MySchema, validate=False)
```

### Memory Optimization
```python
# Use appropriate data types
class OptimizedSchema(BaseSchema):
    ID = SchemaColumn("id", np.int32)          # Instead of int64
    SCORE = SchemaColumn("score", np.float32)  # Instead of float64
    IS_ACTIVE = SchemaColumn("is_active", np.bool_)  # Efficient boolean
```

### Bulk Operations
```python
# Batch validation
errors = []
for chunk in pd.read_csv("large_file.csv", chunksize=10000):
    chunk_errors = MySchema.validate_dataframe(chunk)
    errors.extend(chunk_errors)
```

---

This API reference covers all the core functionality of PandasSchemaster. For more examples and tutorials, see the [examples directory](examples/) and [documentation](docs/).
