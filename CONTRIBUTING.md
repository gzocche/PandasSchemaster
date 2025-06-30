# Contributing to PandasSchemaster

Thank you for your interest in contributing to PandasSchemaster! 🎉

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/PandasSchemaster.git
   cd PandasSchemaster
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install development dependencies**:
   ```bash
   pip install -e .
   pip install -r requirements.txt
   pip install pytest pytest-cov black flake8
   ```

## 🛠️ Development Workflow

### Setting Up Your Development Environment

1. **Install the package in development mode**:
   ```bash
   pip install -e .
   ```

2. **Run tests to ensure everything works**:
   ```bash
   python -m pytest tests/ -v
   ```

3. **Check code coverage**:
   ```bash
   python -m pytest tests/ --cov=pandasschemaster --cov-report=html
   ```

### Making Changes

1. **Create a new branch** for your feature/bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b bugfix/your-bugfix-name
   ```

2. **Make your changes** following our coding standards:
   - Write clear, self-documenting code
   - Add docstrings to all public functions and classes
   - Follow PEP 8 style guidelines
   - Add type hints where appropriate

3. **Write tests** for your changes:
   - Add unit tests in the `tests/` directory
   - Ensure all existing tests still pass
   - Aim for 95%+ code coverage

4. **Format your code**:
   ```bash
   black pandasschemaster/ tests/
   flake8 pandasschemaster/ tests/
   ```

5. **Run the full test suite**:
   ```bash
   python -m pytest tests/ -v --cov=pandasschemaster
   ```

## 📝 Code Style Guidelines

### Python Code Style
- Follow [PEP 8](https://pep8.org/) guidelines
- Use `black` for code formatting (line length: 88 characters)
- Use meaningful variable and function names
- Add type hints for function parameters and return values

### Documentation Style
- Write clear docstrings for all public APIs
- Use Google-style docstrings
- Include examples in docstrings where helpful
- Keep README and documentation up to date

### Example Function Documentation:
```python
def validate_schema(df: pd.DataFrame, schema: BaseSchema) -> List[str]:
    """
    Validate a DataFrame against a schema definition.
    
    Args:
        df: The pandas DataFrame to validate
        schema: The schema class containing column definitions
        
    Returns:
        List of validation error messages (empty if valid)
        
    Example:
        >>> errors = validate_schema(df, SensorSchema)
        >>> if errors:
        ...     print(f"Validation failed: {errors}")
    """
```

## 🧪 Testing Guidelines

### Writing Tests
- Write tests for all new functionality
- Use descriptive test names that explain what is being tested
- Group related tests in the same test class
- Use fixtures for common test data setup

### Test Structure:
```python
def test_schema_column_validation_with_valid_data():
    """Test that SchemaColumn accepts valid data types."""
    # Arrange
    column = SchemaColumn("test_col", np.float64)
    valid_data = [1.0, 2.5, 3.14]
    
    # Act
    result = column.validate(valid_data)
    
    # Assert
    assert result is True
```

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_schema_column.py

# Run with verbose output
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=pandasschemaster --cov-report=term-missing
```

## 📋 Pull Request Process

1. **Ensure your code passes all tests**:
   ```bash
   python -m pytest tests/ -v
   black --check pandasschemaster/ tests/
   flake8 pandasschemaster/ tests/
   ```

2. **Update documentation** if needed:
   - Update README.md for new features
   - Add docstrings to new functions/classes
   - Update examples if API changes

3. **Create a Pull Request**:
   - Use a clear, descriptive title
   - Describe what your PR does and why
   - Reference any related issues
   - Include screenshots for UI changes (if applicable)

4. **PR Template**:
   ```markdown
   ## Description
   Brief description of changes made.
   
   ## Type of Change
   - [ ] Bug fix (non-breaking change which fixes an issue)
   - [ ] New feature (non-breaking change which adds functionality)
   - [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added for new functionality
   - [ ] Code coverage remains above 95%
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Comments added for hard-to-understand areas
   - [ ] Documentation updated
   ```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Python version** and **pandas version**
2. **PandasSchemaster version**
3. **Minimal code example** that reproduces the issue
4. **Expected behavior** vs **actual behavior**
5. **Full error traceback** if applicable

### Bug Report Template:
```markdown
**Environment:**
- Python version: 
- Pandas version: 
- PandasSchemaster version: 
- Operating System: 

**Description:**
A clear description of the bug.

**Minimal Example:**
```python
# Code that reproduces the issue
```

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Error Message:**
```
Full error traceback here
```
```

## 💡 Suggesting Features

We welcome feature suggestions! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the use case** that would benefit from this feature
3. **Provide examples** of how the feature would be used
4. **Consider backwards compatibility**

## 🏷️ Release Process

### Version Numbering
We follow [Semantic Versioning](https://semver.org/):
- **MAJOR**: Breaking changes
- **MINOR**: New features (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number updated in `pyproject.toml`
- [ ] CHANGELOG.md updated
- [ ] Git tag created
- [ ] PyPI package published

## 🎯 Areas Looking for Contributions

We especially welcome contributions in these areas:

### 🚀 High Priority
- [ ] Performance optimizations for large DataFrames
- [ ] Additional file format support (ORC, Avro, etc.)
- [ ] Schema migration utilities
- [ ] Better error messages and debugging tools

### 🔧 Medium Priority
- [ ] Integration with popular data validation libraries
- [ ] Schema versioning and compatibility checking
- [ ] Advanced type inference improvements
- [ ] Documentation and tutorial improvements

### 🌟 Nice to Have
- [ ] GUI schema designer
- [ ] Integration with data pipeline tools
- [ ] Schema registry integration
- [ ] Additional CLI features

## 📚 Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [PEP 8 Style Guide](https://pep8.org/)

## 🤝 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/). Please be respectful and inclusive in all interactions.

## ❓ Questions?

- **General questions**: Start a [GitHub Discussion](https://github.com/gzocche/PandasSchemaster/discussions)
- **Bug reports**: Create a [GitHub Issue](https://github.com/gzocche/PandasSchemaster/issues)
- **Feature requests**: Create a [GitHub Issue](https://github.com/gzocche/PandasSchemaster/issues) with the "enhancement" label

Thank you for contributing to PandasSchemaster! 🙏
