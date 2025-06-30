"""
PandasSchemaster - Type-safe DataFrame library with schema validation

A pandas wrapper that provides schema validation, type safety, and automatic
data conversion based on predefined schema columns. Supports column access
using SchemaColumn objects for maximum type safety.

Includes Entity Framework-like schema generation from data files.
"""

__version__ = "1.0.1"

from .schema_column import SchemaColumn
from .base_schema import BaseSchema
from .schema_dataframe import SchemaDataFrame
from .schema_generator import SchemaGenerator

__all__ = [
    "SchemaColumn",
    "SchemaDataFrame", 
    "BaseSchema",
    "SchemaGenerator",
]
