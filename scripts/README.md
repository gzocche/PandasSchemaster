# PandasSchemaster Generator CLI & MCP Server

A comprehensive command-line toolkit for generating schema classes from data files and running an MCP server for AI assistant integration.

## 🚀 Quick Start

### Option 1: Individual Scripts
```bash
# Generate schema using the dedicated script
python generate_schema.py data.csv -o schema.py

# Start MCP server using the dedicated script
python generate_schema_mcp_server.py
```

### Option 2: Unified PandasSchemstart Interface (Recommended)
```bash
# Generate schema using unified interface
python pandaschemstart.py generate data.csv -o schema.py

# Start MCP server using unified interface
python pandaschemstart.py mcp-server
```

### Option 3: Platform-Specific Wrappers
```bash
# Windows
pandaschemstart.bat generate data.csv -o schema.py
pandaschemstart.bat mcp-server

# Unix/Linux/macOS
./pandaschemstart.sh generate data.csv -o schema.py
./pandaschemstart.sh mcp-server
```

## 📋 Available Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `pandaschemstart.py` | **Unified interface** for all functionality | `python pandaschemstart.py [command] [options]` |
| `generate_schema.py` | Generate schema classes from data files | `python generate_schema.py [file] [options]` |
| `generate_schema_mcp_server.py` | MCP server for AI assistant integration | `python generate_schema_mcp_server.py` |
| `pandaschemstart.bat` | Windows batch wrapper | `pandaschemstart.bat [command] [options]` |
| `pandaschemstart.sh` | Unix/Linux/macOS shell wrapper | `./pandaschemstart.sh [command] [options]` |

## 🎯 Schema Generation

### Basic Usage
```bash
# Using unified interface
python pandaschemstart.py generate data.csv
python pandaschemstart.py generate data.csv -o my_schema.py
python pandaschemstart.py generate data.csv -c CustomerSchema

# Using individual script
python generate_schema.py data.csv
python generate_schema.py data.csv -o my_schema.py
python generate_schema.py data.csv -c CustomerSchema
```

### Advanced Options
```bash
# Sample only first 1000 rows for large files
python pandaschemstart.py generate large_data.csv -s 1000

# Enable verbose output
python pandaschemstart.py generate data.csv -v

# Disable nullable inference
python pandaschemstart.py generate data.csv --no-nullable

# Get help
python pandaschemstart.py generate --help
```

## 🤖 MCP Server for AI Assistants

The MCP (Model Context Protocol) server enables AI assistants to generate schemas through tool calls.

### Starting the Server
```bash
# Using unified interface (recommended)
python pandaschemstart.py mcp-server

# Using individual script
python generate_schema_mcp_server.py

# Platform-specific wrappers
pandaschemstart.bat mcp-server        # Windows
./pandaschemstart.sh mcp-server       # Unix/Linux/macOS
```

### Server Features
- **Tool Integration**: Provides `pandasschemaster.generate_schema` tool for AI assistants
- **SSE Transport**: Uses Server-Sent Events for real-time communication
- **Same Functionality**: All CLI features available through MCP interface
- **Background Operation**: Can run in background for continuous availability

### Available MCP Tools

**`pandasschemaster.generate_schema`**
- **Purpose**: Generate schema classes from DataFrame files
- **Parameters**:
  - `absolute_path` (required): Full path to the data file
  - `class_name` (optional): Name for the generated class (default: "TestSchema")
  - `output_path` (optional): Where to save the schema file
  - `sample_size` (optional): Number of rows to analyze (default: 42)

### Server Management
```bash
# Start in background (Windows)
start /b python pandaschemstart.py mcp-server

# Start in background (Unix/Linux/macOS)
python pandaschemstart.py mcp-server &

# Check if running
tasklist | findstr python     # Windows
ps aux | grep pandaschemstart  # Unix/Linux/macOS
```

## 📄 Supported File Formats

- **CSV** (`.csv`) - Comma-separated values
- **Excel** (`.xlsx`, `.xls`) - Microsoft Excel files
- **JSON** (`.json`) - JavaScript Object Notation
- **Parquet** (`.parquet`) - Apache Parquet format
- **TSV/TXT** (`.tsv`, `.txt`) - Tab-separated values

## 🔧 Command Reference

### Unified PandasSchemstart Commands

The `pandaschemstart.py` script provides two main commands:

#### Generate Command
```bash
python pandaschemstart.py generate <input_file> [OPTIONS]
```

**Options:**
| Option | Description | Example |
|--------|-------------|---------|
| `input_file` | Path to data file (required) | `data.csv` |
| `-o, --output` | Output file for schema | `-o schema.py` |
| `-c, --class-name` | Custom class name | `-c CustomerSchema` |
| `-s, --sample-size` | Number of rows to analyze | `-s 1000` |
| `--no-nullable` | Disable nullable inference | `--no-nullable` |
| `-v, --verbose` | Enable detailed logging | `-v` |
| `-h, --help` | Show help message | `-h` |

#### MCP Server Command
```bash
python pandaschemstart.py mcp-server [OPTIONS]
```

**Options:**
| Option | Description | Example |
|--------|-------------|---------|
| `--transport` | Transport protocol | `--transport=sse` |
| `-h, --help` | Show help message | `-h` |

### Individual Script Options

For users who prefer using individual scripts, the same options are available:

**generate_schema.py:**
| Option | Description | Example |
|--------|-------------|---------|
| `input_file` | Path to data file (required) | `data.csv` |
| `-o, --output` | Output file for schema | `-o schema.py` |
| `-c, --class-name` | Custom class name | `-c CustomerSchema` |
| `-s, --sample-size` | Number of rows to analyze | `-s 1000` |
| `--no-nullable` | Disable nullable inference | `--no-nullable` |
| `-v, --verbose` | Enable detailed logging | `-v` |
| `-h, --help` | Show help message | `-h` |

**generate_schema_mcp_server.py:**
- No command-line options (starts server with default SSE transport)

## 📚 Examples

### Schema Generation Examples

#### Basic CSV Processing
```bash
# Using unified interface
python pandaschemstart.py generate customers.csv

# Using individual script
python generate_schema.py customers.csv
```

#### Excel File with Custom Output
```bash
# Using unified interface
python pandaschemstart.py generate sales_data.xlsx -o sales_schema.py -c SalesDataSchema

# Using individual script
python generate_schema.py sales_data.xlsx -o sales_schema.py -c SalesDataSchema
```

#### Large File with Sampling
```bash
# Using unified interface
python pandaschemstart.py generate huge_dataset.csv -s 5000 -v -o dataset_schema.py

# Using individual script
python generate_schema.py huge_dataset.csv -s 5000 -v -o dataset_schema.py
```

#### JSON File Processing
```bash
# Using unified interface
python pandaschemstart.py generate api_response.json -c ApiResponseSchema

# Using individual script
python generate_schema.py api_response.json -c ApiResponseSchema
```

### MCP Server Examples

#### Basic Server Startup
```bash
# Using unified interface
python pandaschemstart.py mcp-server

# Using individual script
python generate_schema_mcp_server.py

# Using platform wrappers
pandaschemstart.bat mcp-server        # Windows
./pandaschemstart.sh mcp-server       # Unix/Linux/macOS
```

#### AI Assistant Integration
When an AI assistant connects to the MCP server, it can call the schema generation tool:

```json
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

## 🎯 Generated Schema Example

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

## 💡 Tips & Best Practices

### Schema Generation Tips
1. **Large Files**: Use `-s` option to sample data for faster processing
2. **Custom Names**: Use `-c` to provide meaningful class names
3. **File Output**: Use `-o` to save schemas to files for reuse
4. **Debugging**: Use `-v` for detailed information about the generation process
5. **Type Inference**: The tool automatically detects numeric, boolean, datetime, and string types

### MCP Server Tips
1. **Background Running**: Start the server in background for continuous availability
2. **AI Integration**: The server works with any MCP-compatible AI assistant
3. **Tool Discovery**: AI assistants can discover available tools automatically
4. **Error Handling**: The server provides clear error messages for troubleshooting

### Choosing the Right Interface
- **Unified Interface (`pandaschemstart.py`)**: Best for users who want both CLI and MCP functionality
- **Individual Scripts**: Good for users who only need specific functionality
- **Platform Wrappers**: Convenient for users who prefer native shell commands

### Performance Considerations
- Use sampling (`-s`) for files larger than 100MB
- For MCP server, consider memory usage with large concurrent requests
- JSON files may be slower to parse than CSV/Parquet formats
