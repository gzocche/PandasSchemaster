"""
Test suite for PandasSchema library core functionality.

This module contains tests for the essential components of the
PandasSchema library: SchemaColumn, BaseSchema, and SchemaDataFrame.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime

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

    def test_schema_column_str_repr(self):
        """Test SchemaColumn string representation."""
        col = SchemaColumn("temperature", np.float64)
        
        assert str(col) == "temperature"
        assert "temperature" in repr(col)
        assert "float64" in repr(col)

    def test_schema_column_cast_value(self):
        """Test SchemaColumn value casting."""
        float_col = SchemaColumn("test", np.float64)
        int_col = SchemaColumn("test", np.int64)
        bool_col = SchemaColumn("test", np.bool_)
        
        assert float_col.cast_value("23.5") == 23.5
        assert int_col.cast_value("42") == 42
        assert bool_col.cast_value("True") is True


class TestBaseSchema:
    """Test cases for BaseSchema class."""

    def test_get_columns(self):
        """Test getting columns from schema class."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        columns = TestSchema.get_columns()
        assert len(columns) == 2
        assert "col1" in columns
        assert "col2" in columns
        assert isinstance(columns["col1"], SchemaColumn)

    def test_get_column_names(self):
        """Test getting column names from schema."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        names = TestSchema.get_column_names()
        assert len(names) == 2
        assert "col1" in names
        assert "col2" in names

    def test_validate_dataframe_success(self):
        """Test successful DataFrame validation."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64, nullable=False)
            COL2 = SchemaColumn("col2", np.int64, nullable=True)
        
        df = pd.DataFrame({
            "col1": [1.0, 2.0, 3.0],
            "col2": [1, 2, None]
        })
        
        errors = TestSchema.validate_dataframe(df)
        assert len(errors) == 0

    def test_validate_dataframe_missing_required_column(self):
        """Test validation with missing required column."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64, nullable=False)
            COL2 = SchemaColumn("col2", np.int64, nullable=False)
        
        df = pd.DataFrame({
            "col1": [1.0, 2.0, 3.0]
            # Missing col2
        })
        
        errors = TestSchema.validate_dataframe(df)
        assert len(errors) == 1
        assert "col2" in errors[0]
        assert "missing" in errors[0].lower()


class TestSchemaDataFrame:
    """Test cases for SchemaDataFrame class."""

    def test_schema_dataframe_creation(self):
        """Test basic SchemaDataFrame creation."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        data = {"col1": [1.0, 2.0], "col2": [1, 2]}
        df = SchemaDataFrame(data, schema_class=TestSchema, validate=True)        
        assert len(df) == 2
        assert isinstance(df, pd.DataFrame)  # It should be a DataFrame
        assert isinstance(df, SchemaDataFrame)  # And also a SchemaDataFrame
        assert df.schema == TestSchema

    def test_schema_dataframe_auto_cast(self):
        """Test automatic type casting."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        data = {"col1": ["1.0", "2.0"], "col2": ["1", "2"]}  # String values
        df = SchemaDataFrame(data, schema_class=TestSchema, validate=False, auto_cast=True)
        
        assert df["col1"].dtype == np.float64
        # Accept both int64 and Int64 as valid integer dtypes
        assert df["col2"].dtype in ["int64", "Int64", np.int64]

    def test_column_access_with_schema_columns(self):
        """Test accessing columns using SchemaColumn objects."""
        class TestSchema(BaseSchema):
            TEMPERATURE = SchemaColumn("temperature", np.float64)
            PRESSURE = SchemaColumn("pressure", np.float64)
        
        data = {"temperature": [23.5, 24.1], "pressure": [1013.2, 1012.8]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        # Test single column access
        temp = df[TestSchema.TEMPERATURE]
        assert len(temp) == 2
        assert temp.iloc[0] == 23.5
        
        # Test multi-column access
        subset = df[[TestSchema.TEMPERATURE, TestSchema.PRESSURE]]
        assert subset.shape == (2, 2)
        assert "temperature" in subset.columns
        assert "pressure" in subset.columns

    def test_column_assignment_with_schema_columns(self):
        """Test assigning values using SchemaColumn objects."""
        class TestSchema(BaseSchema):
            TEMPERATURE = SchemaColumn("temperature", np.float64)
        
        data = {"temperature": [23.5, 24.1]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        # Test assignment
        df[TestSchema.TEMPERATURE] = [25.0, 25.5]
        
        assert df[TestSchema.TEMPERATURE].iloc[0] == 25.0
        assert df[TestSchema.TEMPERATURE].iloc[1] == 25.5

    def test_select_columns(self):
        """Test column selection method."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
            COL3 = SchemaColumn("col3", np.str_)
        
        data = {"col1": [1.0, 2.0], "col2": [1, 2], "col3": ["a", "b"]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        # Select using schema columns
        selected = df.select_columns([TestSchema.COL1, TestSchema.COL2])
        
        assert selected.shape == (2, 2)
        assert "col1" in selected.columns
        assert "col2" in selected.columns
        assert "col3" not in selected.columns

    def test_string_representation(self):
        """Test string representation of SchemaDataFrame."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
        
        data = {"col1": [1.0, 2.0]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        str_repr = str(df)
        assert "1.0" in str_repr
        assert "2.0" in str_repr
        
        repr_str = repr(df)
        assert "SchemaDataFrame" in repr_str
        assert "TestSchema" in repr_str

    def test_dataframe_inheritance(self):
        """Test that SchemaDataFrame behaves like a pandas DataFrame."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        data = {"col1": [1.0, 2.0, 3.0], "col2": [1, 2, 3]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        # Test DataFrame methods work directly
        assert df.shape == (3, 2)
        assert list(df.columns) == ["col1", "col2"]
        assert df.sum()["col1"] == 6.0
        assert df.mean()["col1"] == 2.0
        
        # Test head() and tail()
        head_df = df.head(2)
        assert len(head_df) == 2
        assert isinstance(head_df, SchemaDataFrame)


class TestSchemaColumnOperations:
    """Test schema column operations in real scenarios."""
    
    def test_mathematical_operations(self):
        """Test mathematical operations with schema columns."""
        class SensorSchema(BaseSchema):
            TEMPERATURE = SchemaColumn("temperature", np.float64)
            HUMIDITY = SchemaColumn("humidity", np.float64)
        
        data = {
            "temperature": [23.5, 24.1, 22.8],
            "humidity": [45.2, 46.8, 44.1]
        }
        df = SchemaDataFrame(data, schema_class=SensorSchema)
        
        # Test mathematical operations
        fahrenheit = df[SensorSchema.TEMPERATURE] * 9/5 + 32
        assert len(fahrenheit) == 3
        assert abs(fahrenheit.iloc[0] - 74.3) < 0.1  # 23.5°C ≈ 74.3°F
        
        # Test operations between columns
        comfort = df[SensorSchema.TEMPERATURE] + df[SensorSchema.HUMIDITY] / 10
        assert len(comfort) == 3

    def test_filtering_with_schema_columns(self):
        """Test filtering operations using schema columns."""
        class SensorSchema(BaseSchema):
            TEMPERATURE = SchemaColumn("temperature", np.float64)
            HUMIDITY = SchemaColumn("humidity", np.float64)
        
        data = {
            "temperature": [23.5, 24.1, 25.2],
            "humidity": [45.2, 46.8, 43.9]
        }
        df = SchemaDataFrame(data, schema_class=SensorSchema)
        
        # Test simple filter
        hot_mask = df[SensorSchema.TEMPERATURE] > 24
        assert hot_mask.sum() == 2  # Two readings above 24°C
        
        # Test complex filter
        complex_mask = (df[SensorSchema.TEMPERATURE] > 24) & (df[SensorSchema.HUMIDITY] > 45)
        assert complex_mask.sum() == 1  # One reading matching both conditions

    def test_column_key_resolution(self):
        """Test the _resolve_column_key method."""
        class TestSchema(BaseSchema):
            COL1 = SchemaColumn("col1", np.float64)
            COL2 = SchemaColumn("col2", np.int64)
        
        data = {"col1": [1.0, 2.0], "col2": [1, 2]}
        df = SchemaDataFrame(data, schema_class=TestSchema)
        
        # Test single column resolution
        assert df._resolve_column_key(TestSchema.COL1) == "col1"
        assert df._resolve_column_key("col1") == "col1"
        
        # Test list resolution
        resolved = df._resolve_column_key([TestSchema.COL1, TestSchema.COL2])
        assert resolved == ["col1", "col2"]
        
        # Test mixed list
        resolved = df._resolve_column_key([TestSchema.COL1, "col2"])
        assert resolved == ["col1", "col2"]


if __name__ == "__main__":
    pytest.main([__file__])
