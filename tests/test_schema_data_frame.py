import pytest
import pandas as pd
import numpy as np
from pandas.testing import assert_frame_equal

from pandasschemaster import SchemaDataFrame, SchemaColumn, BaseSchema


class _MockSchema(BaseSchema):
    """
    Mock schema for testing purposes.
    """

    id = SchemaColumn(name="id", dtype=np.int64, nullable=False)
    name = SchemaColumn(name="name", dtype=np.str_, nullable=False)
    age = SchemaColumn(name="age", dtype=np.int64, nullable=True)


class TestSchemaDataFrame:
    """Test cases for SchemaDataFrame class."""

    @pytest.fixture
    def sample_data(self):
        """Sample data for testing."""
        return {
            "id": [1, 2, 3, 4],
            "name": ["Alice", "Bob", "Charlie", "Diana"],
            "age": [25, 30, None, 35],
        }

    @pytest.fixture
    def sample_df(self, sample_data):
        """Sample DataFrame for testing."""
        return pd.DataFrame(sample_data)

    @pytest.fixture
    def schema_df(self, sample_data):
        """Sample SchemaDataFrame with MockSchema."""
        return SchemaDataFrame(sample_data, schema_class=_MockSchema)

    def test_initialization_with_dict(self, sample_data):
        """Test SchemaDataFrame initialization with dictionary data."""
        df = SchemaDataFrame(sample_data, schema_class=_MockSchema)

        assert isinstance(df, SchemaDataFrame)
        assert df.schema == _MockSchema
        assert len(df) == 4
        assert list(df.columns) == ["id", "name", "age"]

    def test_initialization_with_dataframe(self, sample_df):
        """Test SchemaDataFrame initialization with pandas DataFrame."""
        df = SchemaDataFrame(sample_df, schema_class=_MockSchema)

        assert isinstance(df, SchemaDataFrame)
        assert df.schema == _MockSchema
        assert_frame_equal(df.reset_index(drop=True), sample_df.reset_index(drop=True))

    def test_initialization_without_schema(self, sample_data):
        """Test SchemaDataFrame initialization without schema class."""
        df = SchemaDataFrame(sample_data)

        assert isinstance(df, SchemaDataFrame)
        assert df.schema is None
        assert len(df) == 4

    def test_initialization_with_validation_disabled(self, sample_data):
        """Test SchemaDataFrame initialization with validation disabled."""
        df = SchemaDataFrame(sample_data, schema_class=_MockSchema, validate=False)

        assert isinstance(df, SchemaDataFrame)
        assert df.schema == _MockSchema

    def test_auto_cast_columns(self):
        """Test automatic column type casting."""
        data = {
            "id": ["1", "2", "3"],  # String IDs that should be cast to int
            "name": ["Alice", "Bob", "Charlie"],
            "age": ["25", "30", "35"],  # String ages that should be cast to int
        }

        df = SchemaDataFrame(data, schema_class=_MockSchema, auto_cast=True)
        columns = _MockSchema.get_columns()  # Ensure schema is loaded
        for column_name, schema_col in columns.items():
            assert column_name in df.columns

    def test_validation_success(self, sample_data):
        """Test successful validation with valid data."""
        df = SchemaDataFrame(sample_data, schema_class=_MockSchema, validate=True)

        assert isinstance(df, SchemaDataFrame)
        assert len(df) == 4

    def test_validation_failure_missing_required_column(self):
        """Test validation failure when required column is missing."""
        data = {
            "name": ["Alice", "Bob"],
            "age": [25, 30],
            # Missing required 'id' column
        }

        with pytest.raises(ValueError, match="Required column 'id' is missing"):
            SchemaDataFrame(data, schema_class=_MockSchema, validate=True)

    def test_validation_failure_null_in_non_nullable_column(self):
        """Test validation failure when non-nullable column contains null."""
        data = {
            "id": [1, None, 3],  # Null in non-nullable column
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, 30, 35],
        }

        with pytest.raises(
            ValueError, match="contains.*null values but is not nullable"
        ):
            SchemaDataFrame(data, schema_class=_MockSchema, validate=True)

    def test_column_access_with_string(self, schema_df):
        """Test column access using string column names."""
        id_column = schema_df["id"]

        assert isinstance(id_column, pd.Series)
        assert len(id_column) == 4
        assert list(id_column) == [1, 2, 3, 4]

    def test_column_access_with_schema_column(self, schema_df):
        """Test column access using SchemaColumn objects."""
        id_column = schema_df[_MockSchema.id]

        assert isinstance(id_column, pd.Series)
        assert len(id_column) == 4
        assert list(id_column) == [1, 2, 3, 4]

    def test_multiple_column_access_with_strings(self, schema_df):
        """Test multiple column access using string names."""
        subset = schema_df[["id", "name"]]

        assert isinstance(subset, SchemaDataFrame)
        assert list(subset.columns) == ["id", "name"]
        assert len(subset) == 4

    def test_multiple_column_access_with_schema_columns(self, schema_df):
        """Test multiple column access using SchemaColumn objects."""
        subset = schema_df[[_MockSchema.id, _MockSchema.name]]

        assert isinstance(subset, SchemaDataFrame)
        assert list(subset.columns) == ["id", "name"]
        assert len(subset) == 4

    def test_column_assignment_with_string(self, schema_df):
        """Test column assignment using string column names."""
        schema_df["new_column"] = [1, 2, 3, 4]

        assert "new_column" in schema_df.columns
        assert list(schema_df["new_column"]) == [1, 2, 3, 4]

    def test_column_assignment_with_schema_column(self, schema_df):
        """Test column assignment using SchemaColumn objects."""
        schema_df[_MockSchema.age] = [25, 30, 35, 40]

        assert list(schema_df["age"]) == [25, 30, 35, 40]

    def test_select_columns_with_strings(self, schema_df):
        """Test select_columns method with string column names."""
        subset = schema_df.select_columns(["id", "name"])

        assert isinstance(subset, SchemaDataFrame)
        assert list(subset.columns) == ["id", "name"]
        assert len(subset) == 4
        assert subset.schema == _MockSchema

    def test_select_columns_with_schema_columns(self, schema_df):
        """Test select_columns method with SchemaColumn objects."""
        subset = schema_df.select_columns([_MockSchema.id, _MockSchema.name])

        assert isinstance(subset, SchemaDataFrame)
        assert list(subset.columns) == ["id", "name"]
        assert len(subset) == 4
        assert subset.schema == _MockSchema

    def test_select_columns_mixed_types(self, schema_df):
        """Test select_columns method with mixed string and SchemaColumn types."""
        subset = schema_df.select_columns([_MockSchema.id, "name"])

        assert isinstance(subset, SchemaDataFrame)
        assert list(subset.columns) == ["id", "name"]
        assert len(subset) == 4

    def test_repr_with_schema(self, schema_df):
        """Test string representation with schema."""
        repr_str = repr(schema_df)

        assert "SchemaDataFrame" in repr_str
        assert "_MockSchema" in repr_str

    def test_repr_without_schema(self, sample_data):
        """Test string representation without schema."""
        df = SchemaDataFrame(sample_data)
        repr_str = repr(df)

        assert "SchemaDataFrame" in repr_str
        assert "Schema:" not in repr_str

    def test_schema_property(self, schema_df):
        """Test schema property access."""
        assert schema_df.schema == _MockSchema

    def test_schema_property_none(self, sample_data):
        """Test schema property when no schema is set."""
        df = SchemaDataFrame(sample_data)
        assert df.schema is None

    def test_copy_preserves_schema(self, schema_df):
        """Test that copying preserves schema information."""
        copied_df = schema_df.copy()

        assert isinstance(copied_df, SchemaDataFrame)
        assert copied_df.schema == _MockSchema

    def test_slicing_preserves_schema(self, schema_df):
        """Test that slicing preserves schema information."""
        sliced_df = schema_df.iloc[0:2]

        assert isinstance(sliced_df, SchemaDataFrame)
        assert sliced_df.schema == _MockSchema
        assert len(sliced_df) == 2

    def test_filtering_preserves_schema(self, schema_df):
        """Test that filtering preserves schema information."""
        filtered_df = schema_df[schema_df["age"] > 25]

        assert isinstance(filtered_df, SchemaDataFrame)
        assert filtered_df.schema == _MockSchema
        assert len(filtered_df) == 2  # Bob (30) and Diana (35)

    def test_nullable_column_with_nulls(self):
        """Test that nullable columns accept null values."""
        data = {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "age": [25, None, 35],  # Null in nullable column - should be fine
        }

        df = SchemaDataFrame(data, schema_class=_MockSchema, validate=True)
        assert isinstance(df, SchemaDataFrame)
        assert pd.isna(df.iloc[1]["age"])

    def test_constructor_property(self, schema_df):
        """Test that _constructor property returns SchemaDataFrame."""
        assert schema_df._constructor == SchemaDataFrame

    def test_resolve_column_key_with_string(self, schema_df):
        """Test _resolve_column_key method with string input."""
        resolved = schema_df._resolve_column_key("id")
        assert resolved == "id"

    def test_resolve_column_key_with_schema_column(self, schema_df):
        """Test _resolve_column_key method with SchemaColumn input."""
        resolved = schema_df._resolve_column_key(_MockSchema.id)
        assert resolved == "id"

    def test_resolve_column_key_with_list(self, schema_df):
        """Test _resolve_column_key method with list input."""
        resolved = schema_df._resolve_column_key(["id", _MockSchema.name])
        assert resolved == ["id", "name"]

    def test_getitem_returns_schema_dataframe_for_multiple_columns(self, schema_df):
        """Test that __getitem__ returns SchemaDataFrame for multiple columns."""
        result = schema_df[["id", "name"]]

        assert isinstance(result, SchemaDataFrame)
        assert result.schema == _MockSchema

    def test_setitem_with_auto_cast(self, schema_df):
        """Test that __setitem__ auto-casts values when schema column exists."""
        # Set age column with string values that should be cast to int
        schema_df[_MockSchema.age] = ["25", "30", "35", "40"]

        # Values should be cast to integers
        assert all(isinstance(x, (int, np.integer)) for x in schema_df["age"])

    @pytest.mark.parametrize(
        "invalid_data",
        [
            {"id": [1, 2], "name": ["Alice", None]},  # Null in non-nullable name
            {"id": [None, 2], "name": ["Alice", "Bob"]},  # Null in non-nullable id
        ],
    )
    def test_validation_with_various_invalid_data(self, invalid_data):
        """Test validation with various types of invalid data."""
        with pytest.raises(ValueError):
            SchemaDataFrame(invalid_data, schema_class=_MockSchema, validate=True)

    def test_large_dataset_performance(self):
        """Test SchemaDataFrame with larger dataset."""
        n_rows = 1000
        data = {
            "id": range(1, n_rows + 1),
            "name": [f"Person_{i}" for i in range(1, n_rows + 1)],
            "age": [25 + (i % 50) for i in range(n_rows)],
        }

        df = SchemaDataFrame(data, schema_class=_MockSchema)

        assert len(df) == n_rows
        assert isinstance(df, SchemaDataFrame)
        assert df.schema == _MockSchema
