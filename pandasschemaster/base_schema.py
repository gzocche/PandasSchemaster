"""
BaseSchema implementation for PandasSchemaster library.

This module contains the abstract base class for defining DataFrame schemas
with validation capabilities and column introspection.
"""

from typing import Dict, List
from abc import ABC

import pandas as pd

from .schema_column import SchemaColumn


class BaseSchema(ABC):
    """
    Abstract base class for defining DataFrame schemas.

    Subclasses should define class attributes as SchemaColumn instances
    to specify the structure of their DataFrames.
    """

    @classmethod
    def get_columns(cls) -> Dict[str, SchemaColumn]:
        """
        Get all SchemaColumn attributes from the class.

        Returns:
            Dictionary mapping column names to SchemaColumn instances
        """
        columns = {}
        for attr_name in dir(cls):
            attr_value = getattr(cls, attr_name)
            if isinstance(attr_value, SchemaColumn):
                columns[attr_value.name] = attr_value
        return columns

    @classmethod
    def get_column_names(cls) -> List[str]:
        """
        Get list of column names defined in the schema.

        Returns:
            List of column names
        """
        return list(cls.get_columns().keys())

    @classmethod
    def validate_dataframe(cls, df: pd.DataFrame) -> List[str]:
        """
        Validate a DataFrame against this schema.

        Args:
            df: DataFrame to validate

        Returns:
            List of validation error messages
        """
        errors = []
        schema_columns = cls.get_columns()

        # Check for missing required columns
        for column_name, schema_col in schema_columns.items():
            if column_name not in df.columns and not schema_col.nullable:
                errors.append(f"Required column '{column_name}' is missing")

        # Validate existing columns
        for column_name in df.columns:
            if column_name in schema_columns:
                schema_col = schema_columns[column_name]
                series = df[column_name]

                # Check for null values in non-nullable columns
                if not schema_col.nullable and series.isna().any():
                    null_count = series.isna().sum()
                    errors.append(
                        f"Column '{column_name}' contains {null_count}"
                        + " null values but is not nullable"
                    )

                # Validate individual values
                for idx, value in series.items():
                    if not schema_col.validate_value(value):
                        errors.append(
                            f"Invalid value in column '{column_name}' at index {idx}: {value}"
                        )

        return errors
