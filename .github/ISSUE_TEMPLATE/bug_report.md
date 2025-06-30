---
name: Bug Report
about: Create a report to help us improve PandasSchemaster
title: '[BUG] '
labels: bug
assignees: ''

---

## 🐛 Bug Description
A clear and concise description of what the bug is.

## 🔄 Steps to Reproduce
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## ✅ Expected Behavior
A clear and concise description of what you expected to happen.

## ❌ Actual Behavior
A clear and concise description of what actually happened.

## 📋 Minimal Code Example
```python
# Please provide a minimal code example that reproduces the issue
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema
import pandas as pd
import numpy as np

class TestSchema(BaseSchema):
    # Your schema definition here
    pass

# Your code that demonstrates the bug
```

## 🌍 Environment
- **Python version**: [e.g. 3.9.7]
- **PandasSchemaster version**: [e.g. 1.0.0]
- **Pandas version**: [e.g. 2.0.3]
- **NumPy version**: [e.g. 1.24.3]
- **Operating System**: [e.g. Windows 11, macOS 13.0, Ubuntu 20.04]

## 📊 Sample Data
If applicable, provide sample data that reproduces the issue:
```csv
# Sample CSV data or description of data structure
```

## 🔍 Error Message
If applicable, provide the full error traceback:
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
```

## 📸 Screenshots
If applicable, add screenshots to help explain your problem.

## 🔧 Workaround
If you found a temporary workaround, please describe it here.

## 💡 Additional Context
Add any other context about the problem here.

## ✅ Checklist
- [ ] I have searched existing issues to make sure this is not a duplicate
- [ ] I have provided a minimal code example that reproduces the issue
- [ ] I have included my environment details
- [ ] I have included the complete error message (if applicable)
