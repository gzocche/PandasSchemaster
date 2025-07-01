"""
Schema Generator for PandasSchemaster library.

This module provides Entity Framework-like functionality for generating
schema classes from data files (CSV, Excel, JSON, etc.) using pandas
for file reading and type inference.
"""

import argparse
import re
import sys
import logging
from pathlib import Path
from typing import Dict, Optional, Any

import pandas as pd
import numpy as np

from .schema_column import SchemaColumn

logger = logging.getLogger(__name__)


class SchemaGenerator:
    """
    Generates schema classes from data files, similar to Entity Framework's
    database-first approach but for DataFrame schemas.
    """

    # Type mapping from pandas/numpy types to numpy dtypes
    TYPE_MAPPING = {
        "object": np.object_,
        "string": np.str_,
        "int64": np.int64,
        "Int64": np.int64,
        "int32": np.int32,
        "Int32": np.int32,
        "float64": np.float64,
        "Float64": np.float64,
        "float32": np.float32,
        "Float32": np.float32,
        "bool": np.bool_,
        "boolean": np.bool_,
        "datetime64[ns]": np.datetime64,
        "timedelta64[ns]": np.timedelta64,
        "category": np.object_,
    }

    def __init__(self, infer_nullable: bool = True, sample_size: Optional[int] = None):
        """
        Initialize the schema generator.

        Args:
            infer_nullable: Whether to infer nullable columns based on null values
            sample_size: Number of rows to sample for analysis (None for all rows)
        """
        self.infer_nullable = infer_nullable
        self.sample_size = sample_size

    def read_file(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Read a data file using pandas based on file extension.

        Args:
            file_path: Path to the data file
            **kwargs: Additional arguments passed to pandas read functions

        Returns:
            DataFrame containing the data

        Raises:
            ValueError: If file format is not supported
        """
        file_path = Path(file_path)
        extension = file_path.suffix.lower()

        logger.info("Reading file: %s", file_path)

        if extension == ".csv":
            return pd.read_csv(file_path, **kwargs)
        if extension in [".xlsx", ".xls"]:
            return pd.read_excel(file_path, **kwargs)
        if extension == ".json":
            return pd.read_json(file_path, **kwargs)
        if extension == ".parquet":
            return pd.read_parquet(file_path, **kwargs)
        if extension in [".tsv", ".txt"]:
            kwargs.setdefault("sep", "\t")
            return pd.read_csv(file_path, **kwargs)

        raise ValueError(f"Unsupported file format: {extension}")

    def analyze_column(self, series: pd.Series, column_name: str) -> Dict[str, Any]:
        """
        Analyze a pandas Series to determine schema properties.

        Args:
            series: The pandas Series to analyze
            column_name: Name of the column

        Returns:
            Dictionary with column analysis results
        """
        analysis = {
            "name": column_name,
            "dtype": series.dtype,
            "null_count": series.isna().sum(),
            "total_count": len(series),
            "nullable": False,
            "unique_count": series.nunique(),
            "sample_values": [],
        }

        # Determine if column is nullable
        if self.infer_nullable:
            analysis["nullable"] = analysis["null_count"] > 0

        # Get sample values (non-null)
        non_null_values = series.dropna()
        if len(non_null_values) > 0:
            sample_count = min(5, len(non_null_values))
            analysis["sample_values"] = non_null_values.head(sample_count).tolist()

        # Try to infer better types for object columns
        if series.dtype == "object" and len(non_null_values) > 0:
            analysis["dtype"] = self._infer_object_type(non_null_values)

        return analysis

    def _infer_object_type(self, series: pd.Series) -> np.dtype:
        """
        Try to infer a more specific type for object columns.

        Args:
            series: Non-null values from the column

        Returns:
            Inferred numpy dtype
        """
        # Sample a subset for type inference to avoid full column processing
        sample = series.iloc[: min(100, len(series))]

        # Try to convert to numeric
        try:
            numeric_series = pd.to_numeric(sample, errors="raise")
            if (
                numeric_series.dtype in ["int64", "int32"]
                or (numeric_series % 1 == 0).all()
            ):
                return np.int64
            return np.float64
        except (ValueError, TypeError):
            pass

        # Try to convert to datetime - suppress format warnings since we're testing
        # TODO: Remove this try-except block when not testing
        # This is a workaround for testing purposes to avoid format warnings
        try:
            import warnings

            with warnings.catch_warnings():
                warnings.simplefilter("ignore", UserWarning)
                pd.to_datetime(sample, errors="raise")
            return np.datetime64
        except (ValueError, TypeError):
            pass

        # Try to convert to boolean
        if series.nunique() <= 2:
            unique_values = {str(val).lower() for val in series.unique()}
            bool_values = {"true", "false", "1", "0", "yes", "no", "y", "n"}
            if unique_values.issubset(bool_values):
                return np.bool_

        # Default to object/string
        return np.object_

    def generate_schema_columns(self, df: pd.DataFrame) -> Dict[str, SchemaColumn]:
        """
        Generate SchemaColumn objects from a DataFrame.

        Args:
            df: DataFrame to analyze

        Returns:
            Dictionary mapping column names to SchemaColumn objects
        """
        logger.info(
            "Analyzing DataFrame with %d columns and %d rows", len(df.columns), len(df)
        )

        # Sample data if requested
        if self.sample_size and len(df) > self.sample_size:
            df_sample = df.sample(n=self.sample_size, random_state=42)
            logger.info("Using sample of %d rows for analysis", self.sample_size)
        else:
            df_sample = df

        schema_columns = {}

        for column_name in df_sample.columns:
            series = df_sample[column_name]
            analysis = self.analyze_column(series, column_name)

            # Map pandas dtype to numpy dtype
            numpy_dtype = self.TYPE_MAPPING.get(str(analysis["dtype"]), np.object_)

            # Create SchemaColumn
            schema_column = SchemaColumn(
                name=column_name,
                dtype=numpy_dtype,
                nullable=analysis["nullable"],
                description=f"Column with {analysis['unique_count']} unique values",
            )

            schema_columns[column_name] = schema_column
            logger.debug(f"Created schema column: {schema_column}")

        return schema_columns

    def generate_schema_class_code(
        self,
        schema_columns: Dict[str, SchemaColumn],
        class_name: str,
        file_path: Optional[str] = None,
    ) -> str:
        """
        Generate Python code for a schema class.

        Args:
            schema_columns: Dictionary of SchemaColumn objects
            class_name: Name for the generated class
            file_path: Original file path (for documentation)

        Returns:
            Python code as a string
        """
        # Clean class name
        class_name = self._clean_class_name(class_name)

        # Generate imports
        imports = [
            "import numpy as np",
            "from pandasschemaster import BaseSchema, SchemaColumn",
            "",
        ]

        # Generate class definition
        class_def = [
            f"class {class_name}(BaseSchema):",
            f'    """',
            f"    Schema class generated from data file.",
        ]

        if file_path:
            class_def.append(f"    Source: {file_path}")

        class_def.extend(
            [f"    Generated with {len(schema_columns)} columns.", f'    """', ""]
        )

        # Generate column definitions
        for col_name, schema_col in schema_columns.items():
            attr_name = self._clean_attribute_name(col_name)
            dtype_str = self._get_dtype_string(schema_col.dtype)

            class_def.append(f"    {attr_name} = SchemaColumn(")
            class_def.append(f"        name='{col_name}',")
            class_def.append(f"        dtype={dtype_str},")
            class_def.append(f"        nullable={schema_col.nullable},")
            if schema_col.description:
                class_def.append(f"        description='{schema_col.description}'")
            class_def.append("    )")
            class_def.append("")
        code_lines = imports + class_def
        return "\n".join(code_lines)

    def _clean_class_name(self, name: str) -> str:
        """Clean and format a class name."""
        # If a class name is explicitly provided, use it with minimal cleaning
        if (
            not name.endswith(".csv")
            and not name.endswith(".xlsx")
            and not name.endswith(".json")
        ):
            # It's likely an explicit class name, just ensure it's valid
            name = re.sub(r"[^a-zA-Z0-9_]", "", name)
            if name and name[0].isdigit():
                name = f"Schema_{name}"
            return name or "GeneratedSchema"

        # Remove file extension and path
        name = Path(name).stem
        # Replace non-alphanumeric characters with underscores
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        # Ensure it starts with a letter
        if name and name[0].isdigit():
            name = f"Schema_{name}"
        # Convert to PascalCase
        parts = name.split("_")
        name = "".join(word.capitalize() for word in parts if word)
        return name or "GeneratedSchema"

    def _clean_attribute_name(self, name: str) -> str:
        """Clean and format an attribute name."""
        # Replace non-alphanumeric characters with underscores
        name = re.sub(r"[^a-zA-Z0-9_]", "_", name)
        # Ensure it starts with a letter or underscore
        if name and name[0].isdigit():
            name = f"col_{name}"
        # Convert to uppercase
        return name.upper() if name else "UNKNOWN_COLUMN"

    def _get_dtype_string(self, dtype: np.dtype) -> str:
        """Get string representation of numpy dtype for code generation."""
        if dtype == np.object_:
            return "np.object_"
        elif dtype == np.int64:
            return "np.int64"
        elif dtype == np.int32:
            return "np.int32"
        elif dtype == np.float64:
            return "np.float64"
        elif dtype == np.float32:
            return "np.float32"
        elif dtype == np.bool_:
            return "np.bool_"
        elif dtype == np.datetime64:
            return "np.datetime64"
        elif dtype == np.timedelta64:
            return "np.timedelta64"
        else:
            return f"np.dtype('{dtype}')"

    def generate_from_file(
        self,
        file_path: str,
        output_path: Optional[str] = None,
        class_name: Optional[str] = None,
        **read_kwargs,
    ) -> str:
        """
        Generate a schema class from a data file.

        Args:
            file_path: Path to the data file
            output_path: Path where to save the generated schema file
            class_name: Name for the generated class (defaults to filename)
            **read_kwargs: Additional arguments for pandas read functions

        Returns:
            Generated Python code as string
        """
        # Read the file
        df = self.read_file(file_path, **read_kwargs)

        # Generate schema columns
        schema_columns = self.generate_schema_columns(df)

        # Determine class name
        if not class_name:
            class_name = Path(file_path).stem

        # Generate code
        code = self.generate_schema_class_code(schema_columns, class_name, file_path)

        # Save to file if output path provided
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(code)
            logger.info("Schema class saved to: %s", output_path)

        return code


def main():
    """Command-line interface for schema generation."""
    parser = argparse.ArgumentParser(
        description="Generate PandasSchemaster classes from data files"
    )
    parser.add_argument(
        "input_file", help="Path to the input data file (CSV, Excel, JSON, etc.)"
    )
    parser.add_argument(
        "-o", "--output", help="Output file path for the generated schema class"
    )
    parser.add_argument(
        "-c", "--class-name", help="Name for the generated schema class"
    )
    parser.add_argument(
        "-s", "--sample-size", type=int, help="Number of rows to sample for analysis"
    )
    parser.add_argument(
        "--no-nullable", action="store_true", help="Don't infer nullable columns"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose logging"
    )

    args = parser.parse_args()

    # Setup logging
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level, format="%(levelname)s: %(message)s")

    try:
        # Create generator
        generator = SchemaGenerator(
            infer_nullable=not args.no_nullable, sample_size=args.sample_size
        )

        # Generate schema
        code = generator.generate_from_file(
            file_path=args.input_file,
            output_path=args.output,
            class_name=args.class_name,
        )

        # Print to stdout if no output file specified
        if not args.output:
            print(code)

        print("✅ Schema generation completed successfully!")

    except Exception as e:
        logger.error("Schema generation failed: %s", e)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
