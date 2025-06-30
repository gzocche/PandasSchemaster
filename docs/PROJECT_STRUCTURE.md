# 📁 Project Structure

This document explains the organization and structure of the PandasSchemaster project.

## 🏗️ Repository Layout

```
PandasSchemaster/
├── 📄 README.md                    # Main project documentation
├── 📄 LICENSE                      # MIT license
├── 📄 CHANGELOG.md                 # Version history and changes
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 pyproject.toml               # Project configuration and dependencies
├── 📄 setup.py                     # Legacy setuptools configuration
├── 📄 requirements.txt             # Development dependencies
├── 📄 MANIFEST.in                  # Package manifest for distribution
├── 📄 sample_data.csv              # Sample data for testing/demos
│
├── 📂 pandasschemaster/            # Main package directory
│   ├── 📄 __init__.py              # Package initialization and exports
│   ├── 📄 base_schema.py           # BaseSchema abstract class
│   ├── 📄 schema_column.py         # SchemaColumn class definition
│   ├── 📄 schema_dataframe.py      # SchemaDataFrame implementation
│   ├── 📄 schema_generator.py      # Auto schema generation from data
│   └── 📂 __pycache__/             # Python bytecode cache
│
├── 📂 scripts/                     # Command-line tools and utilities
│   ├── 📄 README.md                # Scripts documentation
│   ├── 📄 generate_schema.py       # Main schema generation script
│   ├── 📄 generate_schema.bat      # Windows batch file
│   └── 📄 generate_schema.sh       # Unix/Linux shell script
│
├── 📂 demos/                       # Example code and demonstrations
│   ├── 📄 __init__.py              # Package marker
│   ├── 📄 README_clean.md          # Demo documentation
│   ├── 📄 example.py               # Basic usage example
│   ├── 📄 entity_framework_demo.py # EF-like schema generation demo
│   ├── 📄 debug_schema.py          # Debugging utilities
│   ├── 📄 quick_test.py            # Quick functionality test
│   ├── 📄 test_generator.py        # Generator testing
│   ├── 📂 data/                    # Sample data files
│   │   └── 📄 45655.parquet        # Sample Parquet file
│   └── 📂 schemas/                 # Generated schema examples
│       └── 📄 test_schema.py       # Sample generated schema
│
├── 📂 tests/                       # Test suite
│   ├── 📄 __init__.py              # Test package marker
│   ├── 📄 test_schema_column.py    # SchemaColumn tests
│   ├── 📄 test_schema_generator.py # SchemaGenerator tests
│   ├── 📄 test_schema_data_frame.py # SchemaDataFrame tests
│   └── 📂 __pycache__/             # Test bytecode cache
│
├── 📂 docs/                        # Documentation
│   ├── 📄 API_REFERENCE.md         # Complete API documentation
│   ├── 📄 CLI_USAGE.md             # Command-line usage guide
│   ├── 📄 EXAMPLES.md              # Comprehensive examples
│   └── 📄 SCHEMA_GENERATION.md     # Schema generation guide
│
├── 📂 .github/                     # GitHub-specific files
│   ├── 📂 ISSUE_TEMPLATE/          # Issue templates
│   │   ├── 📄 bug_report.md        # Bug report template
│   │   └── 📄 feature_request.md   # Feature request template
│   └── 📄 pull_request_template.md # PR template
│
└── 📂 pandasschemaster.egg-info/   # Package metadata (auto-generated)
    ├── 📄 PKG-INFO                 # Package information
    ├── 📄 SOURCES.txt              # Source file list
    ├── 📄 dependency_links.txt     # Dependency links
    ├── 📄 requires.txt             # Requirements
    └── 📄 top_level.txt            # Top-level packages
```

## 📦 Core Package (`pandasschemaster/`)

### `__init__.py`
- **Purpose**: Package initialization and public API exports
- **Contents**: Version info, imports, and `__all__` definition
- **Key Exports**: `SchemaColumn`, `BaseSchema`, `SchemaDataFrame`, `SchemaGenerator`

### `schema_column.py`
- **Purpose**: Defines the `SchemaColumn` class for typed column definitions
- **Key Features**:
  - Column name and data type specification
  - Nullable constraints
  - Default values
  - Validation methods
  - Type casting functionality

### `base_schema.py`
- **Purpose**: Abstract base class for schema definitions
- **Key Features**:
  - Schema validation methods
  - Column introspection
  - Metadata management
  - Class-level utility methods

### `schema_dataframe.py`
- **Purpose**: Pandas DataFrame wrapper with schema validation
- **Key Features**:
  - Type-safe column access
  - Schema-based validation
  - Automatic type casting
  - Full pandas compatibility
  - Multi-column selection

### `schema_generator.py`
- **Purpose**: Automatic schema generation from data files
- **Key Features**:
  - Multiple file format support
  - Type inference algorithms
  - Nullable detection
  - Code generation utilities
  - Entity Framework-like functionality

## 🎯 Scripts Directory (`scripts/`)

### `generate_schema.py`
- **Purpose**: Main CLI tool for schema generation
- **Features**:
  - Command-line argument parsing
  - File format detection
  - Schema code generation
  - Output formatting
  - Error handling and logging

### Platform Scripts
- **`generate_schema.bat`**: Windows batch wrapper
- **`generate_schema.sh`**: Unix/Linux shell wrapper
- **Purpose**: Platform-specific convenience scripts

## 🧪 Test Suite (`tests/`)

### Test Organization
- **`test_schema_column.py`**: Unit tests for `SchemaColumn` class
- **`test_schema_data_frame.py`**: Tests for `SchemaDataFrame` functionality  
- **`test_schema_generator.py`**: Tests for schema generation features

### Test Coverage Areas
- Column validation and type casting
- DataFrame operations and compatibility
- Schema generation from various file formats
- Error handling and edge cases
- Performance benchmarks

## 📚 Documentation (`docs/`)

### Documentation Structure
- **`API_REFERENCE.md`**: Complete API documentation with examples
- **`CLI_USAGE.md`**: Comprehensive CLI usage guide
- **`EXAMPLES.md`**: Real-world examples and tutorials
- **`SCHEMA_GENERATION.md`**: Detailed schema generation guide

## 🎪 Demos (`demos/`)

### Demo Organization
- **`example.py`**: Basic usage demonstration
- **`entity_framework_demo.py`**: EF-like schema generation
- **`debug_schema.py`**: Debugging and troubleshooting utilities
- **`quick_test.py`**: Quick functionality verification
- **`test_generator.py`**: Generator testing and validation

### Sample Data
- **`data/`**: Directory containing sample data files
- **`schemas/`**: Directory with generated schema examples

## 🔧 Configuration Files

### `pyproject.toml`
- **Purpose**: Modern Python project configuration
- **Contents**:
  - Build system configuration
  - Project metadata
  - Dependencies
  - Tool configurations
  - Version management

### `setup.py`
- **Purpose**: Legacy setuptools configuration
- **Status**: Maintained for backwards compatibility

### `requirements.txt`
- **Purpose**: Development dependencies
- **Contents**: Testing, linting, and development tools

### `MANIFEST.in`
- **Purpose**: Package distribution manifest
- **Contents**: Files to include in source distributions

## 🏷️ GitHub Integration (`.github/`)

### Issue Templates
- **`bug_report.md`**: Structured bug report template
- **`feature_request.md`**: Feature request template
- **Purpose**: Consistent issue reporting and feature requests

### Pull Request Template
- **`pull_request_template.md`**: PR checklist and guidelines
- **Purpose**: Ensure quality and consistency in contributions

## 📊 File Naming Conventions

### Python Files
- **Snake case**: `schema_column.py`, `schema_generator.py`
- **Descriptive names**: Clear indication of file purpose
- **Module organization**: Logical grouping of related functionality

### Documentation Files
- **UPPERCASE**: `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md`
- **Descriptive**: `API_REFERENCE.md`, `CLI_USAGE.md`
- **Markdown format**: Consistent `.md` extension

### Test Files
- **Prefix**: All test files start with `test_`
- **Mirror structure**: Test files mirror the package structure
- **Descriptive**: Clear indication of what is being tested

## 🔄 Development Workflow

### Local Development
1. **Clone repository**: Get local copy
2. **Install in dev mode**: `pip install -e .`
3. **Run tests**: `python -m pytest tests/`
4. **Make changes**: Edit source files
5. **Test changes**: Run relevant tests
6. **Update docs**: Keep documentation current

### Distribution
1. **Version bump**: Update version in `pyproject.toml`
2. **Update changelog**: Document changes
3. **Build package**: `python -m build`
4. **Test distribution**: Verify package works
5. **Upload to PyPI**: Publish release

## 🎯 Key Design Principles

### Modularity
- **Single responsibility**: Each module has a clear purpose
- **Loose coupling**: Minimal dependencies between modules
- **High cohesion**: Related functionality grouped together

### Extensibility
- **Plugin architecture**: Easy to extend with new features
- **Abstract base classes**: Clear extension points
- **Configuration driven**: Behavior controlled by configuration

### Documentation
- **Self-documenting code**: Clear names and structure
- **Comprehensive docs**: Multiple documentation formats
- **Examples included**: Real-world usage patterns

### Testing
- **High coverage**: Aim for 95%+ test coverage
- **Multiple test types**: Unit, integration, and performance tests
- **Continuous testing**: Automated test execution

This structure supports maintainability, extensibility, and ease of use while following Python packaging best practices.
