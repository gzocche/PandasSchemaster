# 🚀 CLI Usage Guide

Complete guide for the PandasSchemaster command-line schema generator.

## 📋 Overview

The PandasSchemaster CLI automatically generates schema classes from your data files, similar to Entity Framework's database-first approach. It analyzes your data and creates type-safe schema definitions that you can immediately use in your code.

PandasSchemaster also provides an **MCP (Model Context Protocol) server** that enables AI assistants to generate schemas through tool calls, making it easy to integrate schema generation into AI-powered workflows.

## 🎯 Quick Start

### Basic Usage

```bash
# Generate schema from CSV and print to console
python scripts/generate_schema.py data.csv

# Save schema to file
python scripts/generate_schema.py data.csv -o my_schema.py

# Custom class name
python scripts/generate_schema.py data.csv -o schema.py -c CustomerSchema

# Using the unified pandaschemstart script
python scripts/pandaschemstart.py generate data.csv -o schema.py -c CustomerSchema
```

### MCP Server Mode

The MCP server enables AI assistants to generate schemas through tool calls:

```bash
# Start MCP server (SSE transport by default)
python scripts/generate_schema_mcp_server.py

# Using the unified pandaschemstart script
python scripts/pandaschemstart.py mcp-server

# Start with custom host/port (if supported by transport)
python scripts/pandaschemstart.py mcp-server --transport=sse
```

**MCP Server Features:**
- **Tool Integration**: AI assistants can call `pandasschemaster.generate_schema` tool
- **Real-time Generation**: Generate schemas on-demand through tool calls
- **Same Functionality**: All CLI features available through MCP interface
- **SSE Transport**: Uses Server-Sent Events for communication

### Platform-Specific Scripts

#### Windows
```cmd
# Using batch file
scripts\generate_schema.bat data.csv -o schema.py -c MySchema

# Using PowerShell
powershell -ExecutionPolicy Bypass -File scripts\generate_schema.ps1 data.csv
```

#### Unix/Linux/macOS
```bash
# Using shell script
./scripts/generate_schema.sh data.csv -o schema.py -c MySchema

# Make executable first if needed
chmod +x scripts/generate_schema.sh
```

### Unified PandasSchemstart Script

The `pandaschemstart.py` script provides a unified interface for both CLI generation and MCP server functionality:

#### Schema Generation Mode
```bash
# Generate schema (same as generate_schema.py)
python scripts/pandaschemstart.py generate data.csv -o schema.py -c MySchema

# All standard options are supported
python scripts/pandaschemstart.py generate data.csv -s 1000 --verbose
```

#### MCP Server Mode
```bash
# Start MCP server
python scripts/pandaschemstart.py mcp-server

# With specific transport (default: sse)
python scripts/pandaschemstart.py mcp-server --transport=sse
```

#### Help and Information
```bash
# Show main help
python scripts/pandaschemstart.py --help

# Show generate command help
python scripts/pandaschemstart.py generate --help

# Show MCP server help
python scripts/pandaschemstart.py mcp-server --help
```

## 📖 Command Reference

### Syntax
```bash
python scripts/generate_schema.py <input_file> [OPTIONS]
```

### Arguments

#### `input_file` (required)
Path to the data file to analyze.

**Supported formats:**
- CSV (`.csv`)
- Excel (`.xlsx`, `.xls`)
- JSON (`.json`)
- Parquet (`.parquet`)
- TSV/TXT (`.tsv`, `.txt`)

### Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--output` | `-o` | Output file for schema | `-o schema.py` |
| `--class-name` | `-c` | Custom class name | `-c SensorSchema` |
| `--sample-size` | `-s` | Number of rows to analyze | `-s 1000` |
| `--no-nullable` | | Disable nullable inference | `--no-nullable` |
| `--verbose` | `-v` | Enable detailed logging | `-v` |
| `--help` | `-h` | Show help message | `-h` |

## 💡 Examples

### Example 1: Basic CSV Schema Generation

**Input file: `sensors.csv`**
```csv
timestamp,sensor_id,temperature,humidity,active
2024-01-01 00:00:00,1001,23.5,45.2,true
2024-01-01 01:00:00,1002,24.1,46.8,true
2024-01-01 02:00:00,1001,22.8,44.5,false
```

**Command:**
```bash
python scripts/generate_schema.py sensors.csv -o sensor_schema.py -c SensorSchema
```

**Generated output: `sensor_schema.py`**
```python
"""
Auto-generated schema from sensors.csv
Generated on: 2024-01-01 12:00:00
"""

import numpy as np
from pandasschemaster import BaseSchema, SchemaColumn


class SensorSchema(BaseSchema):
    """Schema for sensors.csv"""
    
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    SENSOR_ID = SchemaColumn("sensor_id", np.int64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64, nullable=True)
    HUMIDITY = SchemaColumn("humidity", np.float64, nullable=True)
    ACTIVE = SchemaColumn("active", np.bool_, nullable=True)
```

### Example 2: Large File with Sampling

**Command:**
```bash
python scripts/generate_schema.py large_dataset.csv -s 5000 -v -o schema.py
```

**Output:**
```
📊 Analyzing large_dataset.csv...
🔍 Sampling 5000 rows from 1,000,000 total rows
📈 Detected 15 columns
🎯 Inferred data types:
  - user_id: int64
  - transaction_amount: float64
  - transaction_date: datetime64
  - is_verified: bool
  ...
✅ Schema generated successfully: schema.py
```

### Example 3: Excel File with Multiple Sheets

**Command:**
```bash
python scripts/generate_schema.py financial_data.xlsx -c FinancialSchema -o finance_schema.py
```

**For Excel files with multiple sheets, the tool will:**
1. Automatically detect the first sheet with data
2. Ask you to specify which sheet if multiple sheets found
3. Generate schema based on the selected sheet

### Example 4: JSON Data

**Input file: `api_response.json`**
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "is_active": true,
    "created_at": "2024-01-01T10:00:00Z"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 25,
    "is_active": false,
    "created_at": "2024-01-02T11:00:00Z"
  }
]
```

**Command:**
```bash
python scripts/generate_schema.py api_response.json -c UserSchema -o user_schema.py
```

## 🔧 Advanced Usage



### Batch Processing

Process multiple files in a directory:

```bash
# Windows batch processing
for %f in (*.csv) do python scripts/generate_schema.py "%f" -o "schemas/%~nf_schema.py"

# Unix/Linux batch processing
for file in *.csv; do
    python scripts/generate_schema.py "$file" -o "schemas/${file%.csv}_schema.py"
done
```

### Integration with Build Systems

#### Makefile
```makefile
schemas: data/*.csv
	@echo "Generating schemas..."
	@for file in data/*.csv; do \
		python scripts/generate_schema.py "$$file" -o "schemas/$$(basename $$file .csv)_schema.py"; \
	done
```

#### Python Build Script
```python
import os
import subprocess
from pathlib import Path

def generate_all_schemas():
    data_dir = Path("data")
    schema_dir = Path("schemas")
    schema_dir.mkdir(exist_ok=True)
    
    for data_file in data_dir.glob("*.csv"):
        schema_file = schema_dir / f"{data_file.stem}_schema.py"
        cmd = [
            "python", "scripts/generate_schema.py",
            str(data_file),
            "-o", str(schema_file),
            "-c", f"{data_file.stem.title()}Schema"
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Generated {schema_file}")

if __name__ == "__main__":
    generate_all_schemas()
```

## 🎨 Generated Schema Features

### Automatic Type Detection

The generator intelligently detects:

- **Numeric types**: `int64`, `float64`, `int32`, `float32`
- **Boolean types**: `bool` (from true/false, 1/0, yes/no)
- **Date/time types**: `datetime64` (various formats)
- **String types**: `object` (for text data)
- **Categorical types**: `object` (with suggestions for categories)

### Nullable Inference

```python
# Column with no null values
USER_ID = SchemaColumn("user_id", np.int64, nullable=False)

# Column with null values
MIDDLE_NAME = SchemaColumn("middle_name", np.object_, nullable=True)
```

### Descriptive Comments

```python
class GeneratedSchema(BaseSchema):
    """
    Auto-generated schema from data.csv
    
    Dataset info:
    - Rows analyzed: 10,000
    - Columns: 15
    - Generated: 2024-01-01 12:00:00
    """
    
    # Primary identifier (no nulls detected)
    USER_ID = SchemaColumn("user_id", np.int64, nullable=False)
    
    # Numeric field with possible nulls
    SCORE = SchemaColumn("score", np.float64, nullable=True)
```

## 🐛 Troubleshooting

### Common Issues

#### File Not Found
```bash
Error: File 'data.csv' not found
```
**Solution:** Check file path and ensure file exists.

#### Unsupported File Format
```bash
Error: Unsupported file format: .xyz
```
**Solution:** Use supported formats (CSV, Excel, JSON, Parquet, TSV).

#### Memory Issues with Large Files
```bash
MemoryError: Unable to load large dataset
```
**Solution:** Use sampling with `-s` option:
```bash
python scripts/generate_schema.py huge_file.csv -s 10000
```

#### Permission Errors
```bash
PermissionError: Cannot write to output file
```
**Solution:** Check write permissions for output directory.

### Debug Mode

Enable verbose logging for troubleshooting:

```bash
python scripts/generate_schema.py data.csv -v
```

**Verbose output includes:**
- File reading progress
- Type inference details
- Column analysis results
- Schema generation steps

### Manual Type Override

If automatic type detection isn't perfect, you can manually edit the generated schema:

```python
# Generated (might be incorrect)
PRICE = SchemaColumn("price", np.object_, nullable=True)

# Manual correction
PRICE = SchemaColumn("price", np.float64, nullable=False)
```

## 🔮 Advanced Features

### MCP Server Integration

The MCP (Model Context Protocol) server allows AI assistants to generate schemas through tool calls:

#### Available Tools

**`pandasschemaster.generate_schema`**
- **Purpose**: Generate schema classes from DataFrame files
- **Parameters**:
  - `absolute_path` (required): Full path to the data file
  - `class_name` (optional): Name for the generated class (default: "TestSchema")
  - `output_path` (optional): Where to save the schema file
  - `sample_size` (optional): Number of rows to analyze (default: 42)

#### Usage Examples with AI Assistants

When an AI assistant calls the MCP server:

```python
# Tool call example (AI assistant perspective)
{
    "tool": "pandasschemaster.generate_schema",
    "parameters": {
        "absolute_path": "/path/to/data.csv",
        "class_name": "CustomerSchema",
        "output_path": "/path/to/schema.py",
        "sample_size": 1000
    }
}
```

#### Server Management

```bash
# Start server in background (Windows)
start /b python scripts/pandaschemstart.py mcp-server

# Start server in background (Unix/Linux/macOS)
python scripts/pandaschemstart.py mcp-server &

# Check if server is running
ps aux | grep pandaschemstart  # Unix/Linux/macOS
tasklist | findstr python     # Windows
```

### Custom Type Mapping

You can extend the type mapping by modifying `SchemaGenerator.TYPE_MAPPING`:

```python
# In schema_generator.py
TYPE_MAPPING = {
    # Standard mappings
    "object": np.object_,
    "int64": np.int64,
    
    # Custom mappings
    "decimal": np.float64,  # Treat decimals as float64
    "phone": np.object_,    # Phone numbers as strings
}
```

### Schema Templates

Create reusable schema templates:

```python
# template_generator.py
from pandasschemaster import SchemaGenerator

class CustomSchemaGenerator(SchemaGenerator):
    def __init__(self, template_name: str):
        super().__init__()
        self.template_name = template_name
    
    def generate_with_template(self, file_path: str) -> str:
        base_schema = self.generate_schema_from_file(file_path)
        
        # Add template-specific enhancements
        if self.template_name == "financial":
            base_schema += self._add_financial_methods()
        elif self.template_name == "iot":
            base_schema += self._add_iot_methods()
            
        return base_schema
```

### Integration with IDEs

#### VS Code Task
```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Generate Schema",
            "type": "shell",
            "command": "python",
            "args": [
                "scripts/generate_schema.py",
                "${input:dataFile}",
                "-o",
                "schemas/${input:schemaName}.py",
                "-c",
                "${input:className}"
            ],
            "group": "build",
            "inputs": [
                {
                    "id": "dataFile",
                    "description": "Data file path",
                    "type": "promptString"
                },
                {
                    "id": "schemaName",
                    "description": "Schema file name",
                    "type": "promptString"
                },
                {
                    "id": "className",
                    "description": "Schema class name",
                    "type": "promptString"
                }
            ]
        }
    ]
}
```

## 📊 Performance Considerations

### Large Files
- Use `-s` (sample size) for files > 100MB
- Consider processing in chunks for very large datasets
- Monitor memory usage with `-v` (verbose) flag

### Optimal Sample Sizes
- **Small files** (< 1MB): Use all data
- **Medium files** (1-100MB): Sample 10,000-50,000 rows
- **Large files** (> 100MB): Sample 5,000-10,000 rows

### File Format Performance
1. **Parquet**: Fastest (columnar format)
2. **CSV**: Good (simple format)
3. **JSON**: Moderate (parsing overhead)
4. **Excel**: Slower (complex format)

---

## 🎯 Next Steps

After generating your schema:

1. **Review the generated code** and make manual adjustments if needed
2. **Test with your data** using `SchemaDataFrame`
3. **Integrate into your project** and enjoy type-safe DataFrame operations
4. **Set up automated schema generation** in your CI/CD pipeline

### Integration Options

**Standalone CLI Usage:**
```bash
# Use individual scripts for specific tasks
python scripts/generate_schema.py data.csv -o schema.py
python scripts/generate_schema_mcp_server.py
```

**Unified Interface (Recommended):**
```bash
# Use the unified script for all functionality
python scripts/pandaschemstart.py generate data.csv -o schema.py
python scripts/pandaschemstart.py mcp-server
```

**AI Assistant Integration:**
```bash
# Start MCP server for AI-powered schema generation
python scripts/pandaschemstart.py mcp-server
# Then use any MCP-compatible AI assistant to call:
# - pandasschemaster.generate_schema tool
```

For more examples and advanced usage, see:
- [API Reference](API_REFERENCE.md)
- [Examples Directory](../examples/)
- [Scripts Documentation](../scripts/README.md)
