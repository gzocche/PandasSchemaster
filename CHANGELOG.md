# Changelog

All notable changes to PandasSchemaster will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Performance optimizations for large DataFrames
- Better error messages with suggestions
- Support for schema inheritance

### Changed
- Improved type inference algorithms
- Enhanced CLI output formatting

### Fixed
- Memory leaks with large file processing
- Type casting edge cases

## [1.0.1] - 2025-06-30

### Fixed
- Package publishing issues
- Version synchronization across files

## [1.0.0] - 2024-01-01

### Added
- Initial release of PandasSchemaster
- Core `SchemaColumn` class with type validation
- `BaseSchema` abstract class for schema definitions
- `SchemaDataFrame` with type-safe column access
- `SchemaGenerator` for automatic schema creation from data files
- Command-line schema generation tool
- Support for CSV, Excel, JSON, Parquet, and TSV files
- Comprehensive test suite with 95%+ coverage
- Full pandas DataFrame compatibility
- Type-safe mathematical operations
- Schema-based column filtering and selection
- Automatic type casting and validation
- Nullable column inference
- Default value support
- Column descriptions and metadata

### Features
- 🛡️ Type-safe DataFrame operations
- 🔧 IDE autocompletion support
- ✅ Automatic data validation
- 🔄 Smart type casting
- 🐼 Full pandas compatibility
- 📖 Self-documenting schemas
- 🚀 Entity Framework-like code generation

### Documentation
- Complete API reference
- CLI usage guide
- Contributing guidelines
- Multiple code examples
- Performance tips and best practices

### Dependencies
- pandas >= 2.0.0
- numpy >= 1.24.0
- Python >= 3.8

---

## Version History

### Pre-release Development

#### [0.9.0] - 2023-12-15
- Beta release with core functionality
- Initial schema generation capabilities
- Basic type safety implementation

#### [0.8.0] - 2023-12-01
- Alpha release for testing
- Core SchemaColumn implementation
- Proof of concept validation

#### [0.7.0] - 2023-11-15
- Initial prototype
- Basic column access patterns
- Type mapping experiments

---

## Migration Guide

### From 0.x to 1.0.0

No breaking changes - all 0.x APIs are compatible with 1.0.0.

### Future Migrations

We follow semantic versioning:
- **MAJOR**: Breaking API changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

Breaking changes will be clearly documented with migration guides.

---

## Contributors

Thanks to all contributors who helped make PandasSchemaster possible!

- [@gzocche](https://github.com/gzocche) - Creator and maintainer
- [Community contributors](https://github.com/gzocche/PandasSchemaster/contributors)

---

## License

[MIT License](LICENSE) - see LICENSE file for details.
