"""
Test suite for PandasSchema library.

This module contains comprehensive tests for all components of the
PandasSchema library, ensuring reliability and correctness.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from pandasschemaster.core import SchemaColumn, SchemaDataFrame, BaseSchema


class TestSchemaColumn:
    """Test cases for SchemaColumn class."""

    def test_schema_column_creation(self):
        """Test basic SchemaColumn creation."""
        col = SchemaColumn(
            name="test_column",
            dtype=np.float64,
            nullable=True,
            description="Test column",
        )

        assert col.name == "test_column"
        assert col.dtype == np.float64
        assert col.nullable is True
        assert col.description == "Test column"

    def test_schema_column_validation(self):
        """Test SchemaColumn validation methods."""
        col = SchemaColumn(
            name="temperature",
            dtype=np.float64,
            validator=SchemaValidator.range_validator(0, 100),
        )

        assert col.validate_value(50.0) is True
        assert col.validate_value(150.0) is False
        assert col.validate_value(-10.0) is False

    def test_schema_column_transformation(self):
        """Test SchemaColumn transformation methods."""
        col = SchemaColumn(
            name="temperature",
            dtype=np.float64,
            transformer=DataTransformer.temperature_converter("F", "C"),
        )

        # 32°F should become 0°C
        result = col.transform_value(32.0)
        assert abs(result - 0.0) < 0.01

        # 212°F should become 100°C
        result = col.transform_value(212.0)
        assert abs(result - 100.0) < 0.01

    def test_schema_column_cast_value(self):
        """Test SchemaColumn type casting."""
        # Boolean column
        bool_col = SchemaColumn(name="active", dtype=np.bool_)
        assert bool_col.cast_value(1) is True
        assert bool_col.cast_value(0) is False
        assert bool_col.cast_value("true") is True

        # Integer column
        int_col = SchemaColumn(name="count", dtype=np.int64)
        assert int_col.cast_value("123") == 123
        assert int_col.cast_value(123.7) == 123

        # Float column
        float_col = SchemaColumn(name="value", dtype=np.float64)
        assert float_col.cast_value("123.45") == 123.45
        assert float_col.cast_value(123) == 123.0


class TestBaseSchema:
    """Test cases for BaseSchema class."""

    def setup_method(self):
        """Set up test schema."""

        class TestSchema(BaseSchema):
            ID = SchemaColumn(name="id", dtype=np.int64, nullable=False)
            NAME = SchemaColumn(name="name", dtype=np.dtype("object"), nullable=False)
            VALUE = SchemaColumn(name="value", dtype=np.float64, nullable=True)

        self.TestSchema = TestSchema

    def test_get_columns(self):
        """Test getting columns from schema."""
        columns = self.TestSchema.get_columns()

        assert len(columns) == 3
        assert "id" in columns
        assert "name" in columns
        assert "value" in columns
        assert isinstance(columns["id"], SchemaColumn)

    def test_get_column_names(self):
        """Test getting column names from schema."""
        names = self.TestSchema.get_column_names()

        assert len(names) == 3
        assert "id" in names
        assert "name" in names
        assert "value" in names

    def test_validate_dataframe_success(self):
        """Test successful DataFrame validation."""
        df = pd.DataFrame(
            {"id": [1, 2, 3], "name": ["A", "B", "C"], "value": [1.0, 2.0, None]}
        )

        errors = self.TestSchema.validate_dataframe(df)
        assert len(errors) == 0

    def test_validate_dataframe_missing_required_column(self):
        """Test DataFrame validation with missing required column."""
        df = pd.DataFrame({"name": ["A", "B", "C"], "value": [1.0, 2.0, 3.0]})

        errors = self.TestSchema.validate_dataframe(df)
        assert len(errors) > 0
        assert any("Required column 'id' is missing" in error for error in errors)

    def test_validate_dataframe_null_in_non_nullable(self):
        """Test DataFrame validation with null in non-nullable column."""
        df = pd.DataFrame(
            {"id": [1, None, 3], "name": ["A", "B", "C"], "value": [1.0, 2.0, 3.0]}
        )

        errors = self.TestSchema.validate_dataframe(df)
        assert len(errors) > 0
        assert any("null values but is not nullable" in error for error in errors)


class TestSchemaDataFrame:
    """Test cases for SchemaDataFrame class."""

    def setup_method(self):
        """Set up test schema and data."""

        class TestSchema(BaseSchema):
            ID = SchemaColumn(name="id", dtype=np.int64, nullable=False)
            VALUE = SchemaColumn(name="value", dtype=np.float64, nullable=True)
            ACTIVE = SchemaColumn(name="active", dtype=np.bool_, nullable=True)

        self.TestSchema = TestSchema
        self.test_data = {
            "id": [1, 2, 3],
            "value": [1.5, 2.5, 3.5],
            "active": [True, False, True],
        }

    def test_schema_dataframe_creation(self):
        """Test basic SchemaDataFrame creation."""
        sdf = SchemaDataFrame(
            data=self.test_data,
            schema_class=self.TestSchema,
            validate=True,
            auto_cast=True,
        )

        assert len(sdf) == 3
        assert sdf.schema == self.TestSchema
        assert list(sdf.df.columns) == ["id", "value", "active"]

    def test_schema_dataframe_auto_cast(self):
        """Test automatic type casting."""
        # Data with wrong types
        mixed_data = {
            "id": ["1", "2", "3"],  # String instead of int
            "value": ["1.5", "2.5", "3.5"],  # String instead of float
            "active": [1, 0, 1],  # Int instead of bool
        }

        sdf = SchemaDataFrame(
            data=mixed_data,
            schema_class=self.TestSchema,
            validate=False,  # Skip validation to test auto-cast
            auto_cast=True,
        )

        # Check that types were converted
        assert sdf.df["id"].dtype in [np.int64, "Int64"]
        assert sdf.df["value"].dtype == np.float64
        assert sdf.df["active"].dtype in [np.bool_, "boolean"]

    def test_schema_dataframe_validation_error(self):
        """Test validation error handling."""
        # Create invalid data
        invalid_data = {"id": [1, 2], "value": [1.5, 2.5], "active": [True, False]}

        # Remove required column to trigger validation error
        del invalid_data["id"]

        with pytest.raises(ValueError):
            SchemaDataFrame(
                data=invalid_data, schema_class=self.TestSchema, validate=True
            )

    def test_add_column(self):
        """Test adding new column with schema."""
        sdf = SchemaDataFrame(
            data=self.test_data, schema_class=self.TestSchema, validate=True
        )

        # Add new column
        new_col = SchemaColumn(name="status", dtype=np.dtype("object"))
        sdf.add_column(new_col, data=["OK", "WARNING", "ERROR"])

        assert "status" in sdf.df.columns
        assert len(sdf.df) == 3
        assert list(sdf.df["status"]) == ["OK", "WARNING", "ERROR"]

    def test_select_columns(self):
        """Test column selection."""
        sdf = SchemaDataFrame(
            data=self.test_data, schema_class=self.TestSchema, validate=True
        )

        # Select specific columns
        selected = sdf.select_columns(["id", "value"])

        assert list(selected.df.columns) == ["id", "value"]
        assert len(selected.df) == 3

    def test_fill_missing(self):
        """Test missing value filling."""
        # Data with missing values
        missing_data = {
            "id": [1, 2, 3],
            "value": [1.5, None, 3.5],
            "active": [True, None, True],
        }

        sdf = SchemaDataFrame(
            data=missing_data,
            schema_class=self.TestSchema,
            validate=False,  # Skip validation due to missing values
        )

        # Fill missing values
        filled = sdf.fill_missing(method="ffill")

        assert not filled.df["value"].isna().any()
        assert not filled.df["active"].isna().any()
        assert filled.df.loc[1, "value"] == 1.5  # Forward filled

    def test_export_methods(self):
        """Test data export methods."""
        sdf = SchemaDataFrame(
            data=self.test_data, schema_class=self.TestSchema, validate=True
        )

        # Test to_dict
        dict_data = sdf.to_dict(orient="records")
        assert len(dict_data) == 3
        assert dict_data[0]["id"] == 1

        # Test to_json
        json_data = sdf.to_json(orient="records")
        assert isinstance(json_data, str)
        assert '"id":1' in json_data


class TestValidators:
    """Test cases for validation functions."""

    def test_range_validator(self):
        """Test range validator."""
        validator = SchemaValidator.range_validator(0, 100)

        assert validator(50) is True
        assert validator(0) is True
        assert validator(100) is True
        assert validator(-1) is False
        assert validator(101) is False
        assert validator(None) is True  # NaN values should pass

    def test_length_validator(self):
        """Test length validator."""
        validator = SchemaValidator.length_validator(min_length=2, max_length=10)

        assert validator("hello") is True
        assert validator("hi") is True
        assert validator("this is too long") is False
        assert validator("x") is False
        assert validator(None) is True

    def test_choices_validator(self):
        """Test choices validator."""
        validator = SchemaValidator.choices_validator(["A", "B", "C"])

        assert validator("A") is True
        assert validator("B") is True
        assert validator("D") is False
        assert validator(None) is True

    def test_positive_validator(self):
        """Test positive number validator."""
        validator = SchemaValidator.positive_validator()

        assert validator(1) is True
        assert validator(0.1) is True
        assert validator(0) is False
        assert validator(-1) is False
        assert validator(None) is True

    def test_percentage_validator(self):
        """Test percentage validator."""
        validator = SchemaValidator.percentage_validator()

        assert validator(50) is True
        assert validator(0) is True
        assert validator(100) is True
        assert validator(-1) is False
        assert validator(101) is False


class TestDataTransformers:
    """Test cases for data transformation functions."""

    def test_temperature_converter(self):
        """Test temperature conversion."""
        f_to_c = DataTransformer.temperature_converter("F", "C")
        c_to_f = DataTransformer.temperature_converter("C", "F")
        c_to_k = DataTransformer.temperature_converter("C", "K")

        # Fahrenheit to Celsius
        assert abs(f_to_c(32) - 0) < 0.01
        assert abs(f_to_c(212) - 100) < 0.01

        # Celsius to Fahrenheit
        assert abs(c_to_f(0) - 32) < 0.01
        assert abs(c_to_f(100) - 212) < 0.01

        # Celsius to Kelvin
        assert abs(c_to_k(0) - 273.15) < 0.01

    def test_unit_converter(self):
        """Test unit conversion."""
        m_to_cm = DataTransformer.unit_converter(100)  # meters to centimeters

        assert m_to_cm(1) == 100
        assert m_to_cm(2.5) == 250
        assert m_to_cm(0) == 0

    def test_string_cleaner(self):
        """Test string cleaning transformer."""
        cleaner = DataTransformer.string_cleaner(strip=True, upper=True)

        assert cleaner("  hello  ") == "HELLO"
        assert cleaner("world") == "WORLD"
        assert cleaner("") == ""

    def test_boolean_converter(self):
        """Test boolean conversion transformer."""
        converter = DataTransformer.boolean_converter()

        assert converter(1) is True
        assert converter("true") is True
        assert converter("YES") is True
        assert converter(0) is False
        assert converter("false") is False
        assert converter("NO") is False


class TestRealWorldExamples:
    """Test cases for real-world schema examples."""

    def test_smart_burner_schema(self):
        """Test Smart Burner schema validation."""
        # Valid data
        burner_data = {
            "TIMESTAMP_ID": [20240101100000],
            "TIMESTAMP": [datetime.now()],
            "BURNER_ON": [True],
            "OXYGEN": [3.2],
            "AIR_FLOW": [1250.5],
            "FUEL_FLOW": [89.3],
            "WASTE_GAS_FLOW": [1340.2],
            "WASTE_GAS_TEMPERATURE": [342.1],
            "TEMPERATURE_ZONE_1": [892.4],
            "TEMPERATURE_ZONE_2": [887.9],
        }

        sdf = SchemaDataFrame(
            data=burner_data,
            schema_class=SmartBurnerSchema,
            validate=True,
            auto_cast=True,
        )

        assert len(sdf) == 1
        assert sdf.df["BURNER_ON"].dtype in [np.bool_, "boolean"]
        assert sdf.df["OXYGEN"].dtype == np.float64

    def test_environmental_sensor_schema(self):
        """Test Environmental Sensor schema validation."""
        env_data = {
            "TIMESTAMP_ID": [20240101100000],
            "TIMESTAMP": [datetime.now()],
            "TEMPERATURE": [23.5],
            "HUMIDITY": [65.2],
            "PRESSURE": [1013.25],
            "WIND_SPEED": [5.2],
            "WIND_DIRECTION": [180.0],
        }

        sdf = SchemaDataFrame(
            data=env_data,
            schema_class=EnvironmentalSensorSchema,
            validate=True,
            auto_cast=True,
        )

        assert len(sdf) == 1
        assert 0 <= sdf.df["HUMIDITY"].iloc[0] <= 100
        assert 0 <= sdf.df["WIND_DIRECTION"].iloc[0] <= 360


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
