"""
SchemaDataFrame implementation for PandasSchemaster library.

This module contains the SchemaDataFrame class which extends pandas DataFrame
with schema validation, type safety, and support for SchemaColumn access.
"""

from typing import Optional, Union, Dict, List, Type
import logging

import pandas as pd
import numpy as np

from .base_schema import BaseSchema
from .schema_column import SchemaColumn

logger = logging.getLogger(__name__)


class SchemaDataFrame(pd.DataFrame):
    """
    A pandas DataFrame with schema validation and type safety.

    This class inherits from pandas DataFrame and adds schema-based validation,
    automatic type conversion, and support for column access using SchemaColumn objects.
    Use df[MySchema.COLUMN] for type-safe operations.
    """

    _metadata = ["_schema_class", "_schema_columns"]

    def __init__(
        self,
        data: Optional[Union[pd.DataFrame, Dict, List]] = None,
        index=None,
        columns=None,
        dtype=None,
        copy=None,
        schema_class: Optional[Type[BaseSchema]] = None,
        validate: bool = True,
        auto_cast: bool = True,
    ):
        """
        Initialize a SchemaDataFrame.

        Args:
            data: Input data (DataFrame, dict, or list)
            index: Index to use for resulting frame
            columns: Column labels to use for resulting frame
            dtype: Data type to force
            copy: Copy data from inputs
            schema_class: Schema class defining the structure
            validate: Whether to validate data on creation
            auto_cast: Whether to automatically cast columns to schema types
        """
        # Initialize the parent DataFrame
        super().__init__(
            data=data, index=index, columns=columns, dtype=dtype, copy=copy
        )

        # Set schema attributes
        self._schema_class = schema_class
        self._schema_columns = schema_class.get_columns() if schema_class else {}

        # Auto-cast columns if requested
        if auto_cast and self._schema_columns:
            self._auto_cast_columns()

        # Validate if requested
        if validate and self._schema_columns:
            self._validate()

    @property
    def _constructor(self):
        """Return the constructor for this type."""
        return SchemaDataFrame

    @property
    def schema(self) -> Optional[Type[BaseSchema]]:
        """Get the schema class."""
        return getattr(self, "_schema_class", None)

    def _auto_cast_columns(self):
        """Automatically cast columns to their schema-defined types."""
        for column_name, schema_col in self._schema_columns.items():
            if column_name in self.columns:
                logger.debug(
                    "Auto-casting column '%s' to %s", column_name, schema_col.dtype
                )
                self[column_name] = self[column_name].apply(schema_col.cast_value)

                # Set pandas dtype for better performance
                try:
                    if schema_col.dtype == np.bool_:
                        self[column_name] = self[column_name].astype("boolean")
                    elif np.issubdtype(schema_col.dtype, np.integer):
                        self[column_name] = pd.to_numeric(
                            self[column_name], errors="coerce"
                        ).astype("Int64")
                    elif np.issubdtype(schema_col.dtype, np.floating):
                        self[column_name] = pd.to_numeric(
                            self[column_name], errors="coerce"
                        ).astype("float64")
                    elif np.issubdtype(schema_col.dtype, np.datetime64):
                        self[column_name] = pd.to_datetime(
                            self[column_name], errors="coerce"
                        )
                except (ValueError, TypeError, AttributeError) as e:
                    logger.warning(
                        "Failed to set pandas dtype for column '%s': %s", column_name, e
                    )

    def _validate(self):
        """Validate the DataFrame against its schema."""
        if not self._schema_class:
            return

        logger.debug(
            "Validating DataFrame with schema: %s", self._schema_class.__name__
        )
        errors = self._schema_class.validate_dataframe(self)
        if errors:
            logger.warning("Schema validation failed with %d errors", len(errors))
            error_msg = "Schema validation failed:\n" + "\n".join(errors)
            raise ValueError(error_msg)
        logger.debug("Schema validation passed")

    def _resolve_column_key(self, key):
        """
        Resolve column key to column name string.

        Args:
            key: Either a string column name or SchemaColumn object

        Returns:
            Column name as string
        """
        if isinstance(key, SchemaColumn):
            return key.name
        elif isinstance(key, list):
            # Handle list of mixed types (strings and SchemaColumns)
            return [self._resolve_column_key(k) for k in key]
        else:
            return key

    def select_columns(
        self, columns: List[Union[str, SchemaColumn]]
    ) -> "SchemaDataFrame":
        """
        Select specific columns and return a new SchemaDataFrame.

        Args:
            columns: List of column names or SchemaColumn objects

        Returns:
            New SchemaDataFrame with selected columns
        """
        column_names = []
        for col in columns:
            if isinstance(col, SchemaColumn):
                column_names.append(col.name)
            else:
                column_names.append(col)

        # Filter existing columns
        available_columns = [col for col in column_names if col in self.columns]
        selected_df = self[available_columns].copy()

        # Preserve schema information
        if hasattr(selected_df, "_schema_class"):
            selected_df._schema_class = self._schema_class
            selected_df._schema_columns = self._schema_columns

        return selected_df

    def __getitem__(self, key):
        """
        Get column(s) from DataFrame.

        Supports both string column names and SchemaColumn objects:
        - df['column_name']
        - df[MySchema.COLUMN_NAME]
        - df[['col1', 'col2']]
        - df[[MySchema.COL1, MySchema.COL2]]
        """
        resolved_key = self._resolve_column_key(key)
        result = super().__getitem__(resolved_key)

        # If result is a DataFrame, preserve schema information
        if isinstance(result, pd.DataFrame) and not isinstance(result, SchemaDataFrame):
            result = SchemaDataFrame(
                data=result,
                schema_class=self._schema_class,
                validate=False,
                auto_cast=False,
            )

        return result

    def __setitem__(self, key, value):
        """
        Set column data in DataFrame.

        Supports both string column names and SchemaColumn objects:
        - df['column_name'] = values
        - df[MySchema.COLUMN_NAME] = values
        """
        resolved_key = self._resolve_column_key(key)
        super().__setitem__(resolved_key, value)

        # Auto-cast if we have schema info for this column
        if hasattr(self, "_schema_columns") and resolved_key in self._schema_columns:
            schema_col = self._schema_columns[resolved_key]
            super().__setitem__(
                resolved_key, self[resolved_key].apply(schema_col.cast_value)
            )

    def __repr__(self) -> str:
        schema_info = (
            f" (Schema: {self._schema_class.__name__})"
            if getattr(self, "_schema_class", None)
            else ""
        )
        return f"SchemaDataFrame{schema_info}:\n{super().__repr__()}"
