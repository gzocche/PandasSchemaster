"""
PandasSchema - Type-safe DataFrame library with schema validation

A pandas wrapper that provides schema validation, type safety, and automatic
data conversion based on predefined schema columns. Supports column access
using SchemaColumn objects for maximum type safety.
"""

__version__ = "1.0.0"

from .core import SchemaColumn, SchemaDataFrame, BaseSchema

__all__ = [
    "SchemaColumn",
    "SchemaDataFrame", 
    "BaseSchema",
]
