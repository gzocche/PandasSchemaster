"""
SchemaColumn implementation for PandasSchemaster library.

This module contains the SchemaColumn class for type-safe column definitions
with validation capabilities, transformation functions, and type casting.
"""

from dataclasses import dataclass
from typing import Any, Optional, Callable
import logging

import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class SchemaColumn:
    """
    Represents a typed column in a schema with validation capabilities.

    This class defines the structure and constraints for DataFrame columns,
    including data type, validation rules, and transformation functions.

    Attributes:
        name: Column name
        dtype: NumPy data type for the column
        nullable: Whether the column can contain null values
        default: Default value for missing data
        validator: Custom validation function
        transformer: Custom transformation function applied before validation
        description: Human-readable description of the column
    """

    name: str
    dtype: np.dtype
    nullable: bool = True
    default: Any = None
    validator: Optional[Callable[[Any], bool]] = None
    transformer: Optional[Callable[[Any], Any]] = None
    description: str = ""

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"SchemaColumn(name='{self.name}', dtype={self.dtype}, nullable={self.nullable})"

    def validate_value(self, value: Any) -> bool:
        """
        Validate a single value against this column's constraints.

        Args:
            value: Value to validate

        Returns:
            True if value is valid, False otherwise
        """
        # Check nullability
        if pd.isna(value) and not self.nullable:
            return False

        # Skip validation for null values if nullable
        if pd.isna(value) and self.nullable:
            return True

        # Apply custom validator if provided
        if self.validator and not self.validator(value):
            return False

        # Type validation
        try:
            np.array([value]).astype(self.dtype)
            return True
        except (ValueError, TypeError):
            return False

    def transform_value(self, value: Any) -> Any:
        """
        Apply transformation function to a value if defined.

        Args:
            value: Value to transform

        Returns:
            Transformed value
        """
        if self.transformer:
            return self.transformer(value)
        return value

    def cast_value(self, value: Any) -> Any:
        """
        Cast value to the column's data type.

        Args:
            value: Value to cast

        Returns:
            Value cast to the appropriate type
        """
        if pd.isna(value):
            return value

        try:
            # Apply transformation first
            transformed_value = self.transform_value(value)

            # Cast to target dtype
            if self.dtype == np.bool_:
                return bool(transformed_value)
            elif np.issubdtype(self.dtype, np.integer):
                return int(transformed_value)
            elif np.issubdtype(self.dtype, np.floating):
                return float(transformed_value)
            elif np.issubdtype(self.dtype, np.datetime64):
                return pd.to_datetime(transformed_value)
            else:
                return np.array([transformed_value]).astype(self.dtype)[0]
        except (ValueError, TypeError) as e:
            logger.debug("Failed to cast value %r to %s: %s", value, self.dtype, e)
            return self.default if self.default is not None else value
