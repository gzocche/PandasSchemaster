# 🎯 Examples and Tutorials

Real-world examples of using PandasSchemaster for type-safe DataFrame operations.

## 📚 Table of Contents

1. [Basic Examples](#basic-examples)
2. [Real-World Use Cases](#real-world-use-cases)
3. [Advanced Patterns](#advanced-patterns)
4. [Integration Examples](#integration-examples)
5. [Performance Examples](#performance-examples)

---

## 🚀 Basic Examples

### Example 1: IoT Sensor Data

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema

# Define schema for IoT sensor data
class IoTSensorSchema(BaseSchema):
    """Schema for IoT sensor readings"""
    DEVICE_ID = SchemaColumn("device_id", np.object_, nullable=False)
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64, nullable=True)
    HUMIDITY = SchemaColumn("humidity", np.float64, nullable=True)
    BATTERY_LEVEL = SchemaColumn("battery_level", np.int64, nullable=True)
    IS_ONLINE = SchemaColumn("is_online", np.bool_, nullable=False, default=True)

# Sample data
sensor_data = {
    'device_id': ['TEMP_001', 'TEMP_002', 'TEMP_001', 'TEMP_003'],
    'timestamp': [
        datetime.now() - timedelta(hours=3),
        datetime.now() - timedelta(hours=2),
        datetime.now() - timedelta(hours=1),
        datetime.now()
    ],
    'temperature': [23.5, 24.1, 22.8, 25.2],
    'humidity': [45.2, 46.8, 44.1, 47.5],
    'battery_level': [85, 92, 78, 88],
    'is_online': [True, True, False, True]
}

# Create validated DataFrame
df = SchemaDataFrame(sensor_data, IoTSensorSchema, validate=True)

# Type-safe operations
print("🌡️ Temperature Analysis")
print(f"Average temperature: {df[IoTSensorSchema.TEMPERATURE].mean():.1f}°C")
print(f"Max temperature: {df[IoTSensorSchema.TEMPERATURE].max():.1f}°C")

# Filter hot readings
hot_readings = df[df[IoTSensorSchema.TEMPERATURE] > 24]
print(f"Hot readings: {len(hot_readings)} devices")

# Multi-column analysis
comfort_index = (
    df[IoTSensorSchema.TEMPERATURE] - 20 + 
    (50 - df[IoTSensorSchema.HUMIDITY]) / 10
)
print(f"Comfort scores: {comfort_index.round(2).tolist()}")

# Battery analysis
low_battery = df[df[IoTSensorSchema.BATTERY_LEVEL] < 80]
print(f"Low battery devices: {low_battery[IoTSensorSchema.DEVICE_ID].tolist()}")
```

### Example 2: Financial Data Analysis

```python
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema
import pandas as pd
import numpy as np

class StockSchema(BaseSchema):
    """Schema for stock market data"""
    SYMBOL = SchemaColumn("symbol", np.object_, nullable=False)
    DATE = SchemaColumn("date", np.datetime64, nullable=False)
    OPEN = SchemaColumn("open", np.float64, nullable=False)
    HIGH = SchemaColumn("high", np.float64, nullable=False)
    LOW = SchemaColumn("low", np.float64, nullable=False)
    CLOSE = SchemaColumn("close", np.float64, nullable=False)
    VOLUME = SchemaColumn("volume", np.int64, nullable=False)
    ADJUSTED_CLOSE = SchemaColumn("adjusted_close", np.float64, nullable=True)

# Sample financial data
stock_data = {
    'symbol': ['AAPL', 'AAPL', 'GOOGL', 'GOOGL', 'MSFT', 'MSFT'],
    'date': pd.date_range('2024-01-01', periods=6, freq='D')[:6],
    'open': [150.0, 152.5, 2800.0, 2850.0, 350.0, 355.0],
    'high': [155.0, 157.0, 2900.0, 2950.0, 360.0, 365.0],
    'low': [148.0, 151.0, 2750.0, 2800.0, 345.0, 350.0],
    'close': [152.5, 156.0, 2850.0, 2900.0, 355.0, 362.0],
    'volume': [1000000, 1200000, 800000, 900000, 1100000, 1300000],
    'adjusted_close': [152.5, 156.0, 2850.0, 2900.0, 355.0, 362.0]
}

df = SchemaDataFrame(stock_data, StockSchema, validate=True)

# Calculate daily returns using schema columns
df['daily_return'] = (
    df[StockSchema.CLOSE] - df[StockSchema.OPEN]
) / df[StockSchema.OPEN] * 100

# Calculate volatility (high-low range)
df['volatility'] = (
    df[StockSchema.HIGH] - df[StockSchema.LOW]
) / df[StockSchema.OPEN] * 100

# Find high-volume trading days
high_volume_threshold = df[StockSchema.VOLUME].quantile(0.75)
high_volume_days = df[df[StockSchema.VOLUME] > high_volume_threshold]

print("📈 Financial Analysis Results")
print(f"Average daily return: {df['daily_return'].mean():.2f}%")
print(f"High volume days: {len(high_volume_days)}")
print(f"Most volatile stock: {df.loc[df['volatility'].idxmax(), StockSchema.SYMBOL.name]}")
```

---

## 🏢 Real-World Use Cases

### Use Case 1: Customer Analytics Pipeline

```python
import pandas as pd
import numpy as np
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema, SchemaGenerator

class CustomerSchema(BaseSchema):
    """Customer analytics schema"""
    CUSTOMER_ID = SchemaColumn("customer_id", np.int64, nullable=False)
    EMAIL = SchemaColumn("email", np.object_, nullable=False)
    FIRST_NAME = SchemaColumn("first_name", np.object_, nullable=True)
    LAST_NAME = SchemaColumn("last_name", np.object_, nullable=True)
    REGISTRATION_DATE = SchemaColumn("registration_date", np.datetime64, nullable=False)
    LAST_LOGIN = SchemaColumn("last_login", np.datetime64, nullable=True)
    TOTAL_PURCHASES = SchemaColumn("total_purchases", np.int64, nullable=False, default=0)
    LIFETIME_VALUE = SchemaColumn("lifetime_value", np.float64, nullable=False, default=0.0)
    IS_PREMIUM = SchemaColumn("is_premium", np.bool_, nullable=False, default=False)
    CHURN_RISK = SchemaColumn("churn_risk", np.float64, nullable=True)

def analyze_customer_data(file_path: str):
    """Complete customer analytics pipeline"""
    
    # 1. Auto-generate schema from data (optional - for new datasets)
    # generator = SchemaGenerator()
    # auto_schema = generator.generate_schema_from_file(file_path)
    # print("Auto-generated schema:", auto_schema)
    
    # 2. Load and validate data
    df = pd.read_csv(file_path)
    customers = SchemaDataFrame(df, CustomerSchema, validate=True, auto_cast=True)
    
    # 3. Data quality checks using schema
    validation_errors = customers.validate_against_schema()
    if validation_errors:
        print("❌ Data quality issues found:")
        for error in validation_errors:
            print(f"  - {error}")
        return None
    
    # 4. Customer segmentation using schema columns
    # High-value customers
    high_value = customers[customers[CustomerSchema.LIFETIME_VALUE] > 1000]
    
    # Recent customers (registered in last 30 days)
    thirty_days_ago = pd.Timestamp.now() - pd.Timedelta(days=30)
    recent_customers = customers[
        customers[CustomerSchema.REGISTRATION_DATE] > thirty_days_ago
    ]
    
    # At-risk customers (high churn risk)
    at_risk = customers[
        (customers[CustomerSchema.CHURN_RISK] > 0.7) & 
        (customers[CustomerSchema.IS_PREMIUM] == True)
    ]
    
    # 5. Analytics calculations
    analytics = {
        'total_customers': len(customers),
        'high_value_customers': len(high_value),
        'recent_signups': len(recent_customers),
        'at_risk_premium': len(at_risk),
        'avg_lifetime_value': customers[CustomerSchema.LIFETIME_VALUE].mean(),
        'premium_conversion_rate': customers[CustomerSchema.IS_PREMIUM].mean() * 100
    }
    
    # 6. Generate insights
    print("👥 Customer Analytics Dashboard")
    print("=" * 40)
    print(f"Total Customers: {analytics['total_customers']:,}")
    print(f"High-Value Customers: {analytics['high_value_customers']:,}")
    print(f"Recent Signups (30d): {analytics['recent_signups']:,}")
    print(f"At-Risk Premium: {analytics['at_risk_premium']:,}")
    print(f"Avg Lifetime Value: ${analytics['avg_lifetime_value']:,.2f}")
    print(f"Premium Conversion: {analytics['premium_conversion_rate']:.1f}%")
    
    return {
        'data': customers,
        'segments': {
            'high_value': high_value,
            'recent': recent_customers,
            'at_risk': at_risk
        },
        'analytics': analytics
    }

# Usage
# results = analyze_customer_data('customer_data.csv')
```

### Use Case 2: Manufacturing Quality Control

```python
class QualityControlSchema(BaseSchema):
    """Manufacturing quality control schema"""
    BATCH_ID = SchemaColumn("batch_id", np.object_, nullable=False)
    PRODUCTION_LINE = SchemaColumn("production_line", np.int64, nullable=False)
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    TEMPERATURE = SchemaColumn("temperature", np.float64, nullable=False)
    PRESSURE = SchemaColumn("pressure", np.float64, nullable=False)
    HUMIDITY = SchemaColumn("humidity", np.float64, nullable=False)
    DEFECT_COUNT = SchemaColumn("defect_count", np.int64, nullable=False, default=0)
    PASS_RATE = SchemaColumn("pass_rate", np.float64, nullable=False)
    OPERATOR_ID = SchemaColumn("operator_id", np.object_, nullable=False)
    SHIFT = SchemaColumn("shift", np.object_, nullable=False)

def quality_control_analysis(df: SchemaDataFrame):
    """Manufacturing quality analysis with type safety"""
    
    # Control limits for process parameters
    TEMP_LIMITS = (18, 25)  # Celsius
    PRESSURE_LIMITS = (0.8, 1.2)  # Bar
    HUMIDITY_LIMITS = (40, 60)  # %
    
    # Identify out-of-spec conditions using schema columns
    temp_violations = df[
        (df[QualityControlSchema.TEMPERATURE] < TEMP_LIMITS[0]) |
        (df[QualityControlSchema.TEMPERATURE] > TEMP_LIMITS[1])
    ]
    
    pressure_violations = df[
        (df[QualityControlSchema.PRESSURE] < PRESSURE_LIMITS[0]) |
        (df[QualityControlSchema.PRESSURE] > PRESSURE_LIMITS[1])
    ]
    
    humidity_violations = df[
        (df[QualityControlSchema.HUMIDITY] < HUMIDITY_LIMITS[0]) |
        (df[QualityControlSchema.HUMIDITY] > HUMIDITY_LIMITS[1])
    ]
    
    # Quality metrics by production line
    line_metrics = df.groupby(QualityControlSchema.PRODUCTION_LINE.name).agg({
        QualityControlSchema.PASS_RATE.name: ['mean', 'std'],
        QualityControlSchema.DEFECT_COUNT.name: 'sum',
        QualityControlSchema.BATCH_ID.name: 'count'
    }).round(2)
    
    # Operator performance analysis
    operator_performance = df.groupby(QualityControlSchema.OPERATOR_ID.name).agg({
        QualityControlSchema.PASS_RATE.name: 'mean',
        QualityControlSchema.DEFECT_COUNT.name: 'mean'
    }).round(2)
    
    # Shift analysis
    shift_analysis = df.groupby(QualityControlSchema.SHIFT.name).agg({
        QualityControlSchema.PASS_RATE.name: 'mean',
        QualityControlSchema.TEMPERATURE.name: 'mean',
        QualityControlSchema.PRESSURE.name: 'mean'
    }).round(2)
    
    print("🏭 Quality Control Analysis")
    print("=" * 40)
    print(f"Temperature violations: {len(temp_violations)}")
    print(f"Pressure violations: {len(pressure_violations)}")
    print(f"Humidity violations: {len(humidity_violations)}")
    print(f"Overall pass rate: {df[QualityControlSchema.PASS_RATE].mean():.1f}%")
    
    return {
        'violations': {
            'temperature': temp_violations,
            'pressure': pressure_violations,
            'humidity': humidity_violations
        },
        'metrics': {
            'by_line': line_metrics,
            'by_operator': operator_performance,
            'by_shift': shift_analysis
        }
    }
```

### Use Case 3: E-commerce Order Processing

```python
class OrderSchema(BaseSchema):
    """E-commerce order processing schema"""
    ORDER_ID = SchemaColumn("order_id", np.object_, nullable=False)
    CUSTOMER_ID = SchemaColumn("customer_id", np.int64, nullable=False)
    ORDER_DATE = SchemaColumn("order_date", np.datetime64, nullable=False)
    SHIP_DATE = SchemaColumn("ship_date", np.datetime64, nullable=True)
    TOTAL_AMOUNT = SchemaColumn("total_amount", np.float64, nullable=False)
    DISCOUNT_AMOUNT = SchemaColumn("discount_amount", np.float64, nullable=False, default=0.0)
    TAX_AMOUNT = SchemaColumn("tax_amount", np.float64, nullable=False)
    SHIPPING_COST = SchemaColumn("shipping_cost", np.float64, nullable=False, default=0.0)
    STATUS = SchemaColumn("status", np.object_, nullable=False)
    PAYMENT_METHOD = SchemaColumn("payment_method", np.object_, nullable=False)
    SHIPPING_ADDRESS_STATE = SchemaColumn("shipping_address_state", np.object_, nullable=False)

def process_order_analytics(orders_df: SchemaDataFrame):
    """E-commerce order analytics pipeline"""
    
    # Calculate derived metrics using schema columns
    orders_df['net_revenue'] = (
        orders_df[OrderSchema.TOTAL_AMOUNT] - 
        orders_df[OrderSchema.DISCOUNT_AMOUNT]
    )
    
    orders_df['fulfillment_time'] = (
        orders_df[OrderSchema.SHIP_DATE] - 
        orders_df[OrderSchema.ORDER_DATE]
    ).dt.days
    
    # Revenue analysis by state
    state_revenue = orders_df.groupby(
        OrderSchema.SHIPPING_ADDRESS_STATE.name
    ).agg({
        'net_revenue': ['sum', 'mean', 'count'],
        OrderSchema.TOTAL_AMOUNT.name: 'sum'
    }).round(2)
    
    # Payment method analysis
    payment_analysis = orders_df.groupby(
        OrderSchema.PAYMENT_METHOD.name
    ).agg({
        OrderSchema.ORDER_ID.name: 'count',
        'net_revenue': 'sum',
        OrderSchema.TOTAL_AMOUNT.name: 'mean'
    }).round(2)
    
    # Order status distribution
    status_dist = orders_df[OrderSchema.STATUS.name].value_counts()
    
    # Time-based analysis
    orders_df['order_month'] = orders_df[OrderSchema.ORDER_DATE].dt.to_period('M')
    monthly_trends = orders_df.groupby('order_month').agg({
        OrderSchema.ORDER_ID.name: 'count',
        'net_revenue': 'sum',
        'fulfillment_time': 'mean'
    }).round(2)
    
    print("🛒 E-commerce Analytics Dashboard")
    print("=" * 40)
    print(f"Total Orders: {len(orders_df):,}")
    print(f"Total Revenue: ${orders_df['net_revenue'].sum():,.2f}")
    print(f"Average Order Value: ${orders_df['net_revenue'].mean():.2f}")
    print(f"Average Fulfillment Time: {orders_df['fulfillment_time'].mean():.1f} days")
    
    return {
        'summary': {
            'total_orders': len(orders_df),
            'total_revenue': orders_df['net_revenue'].sum(),
            'avg_order_value': orders_df['net_revenue'].mean(),
            'avg_fulfillment_time': orders_df['fulfillment_time'].mean()
        },
        'analysis': {
            'by_state': state_revenue,
            'by_payment_method': payment_analysis,
            'status_distribution': status_dist,
            'monthly_trends': monthly_trends
        }
    }
```

---

## 🔧 Advanced Patterns

### Pattern 1: Schema Inheritance

```python
# Base schema for common fields
class BaseEntitySchema(BaseSchema):
    """Base schema with common audit fields"""
    ID = SchemaColumn("id", np.int64, nullable=False)
    CREATED_AT = SchemaColumn("created_at", np.datetime64, nullable=False)
    UPDATED_AT = SchemaColumn("updated_at", np.datetime64, nullable=True)
    IS_ACTIVE = SchemaColumn("is_active", np.bool_, nullable=False, default=True)

# Specific schemas inheriting from base
class UserSchema(BaseEntitySchema):
    """User schema extending base entity"""
    EMAIL = SchemaColumn("email", np.object_, nullable=False)
    USERNAME = SchemaColumn("username", np.object_, nullable=False)
    FIRST_NAME = SchemaColumn("first_name", np.object_, nullable=True)
    LAST_NAME = SchemaColumn("last_name", np.object_, nullable=True)

class ProductSchema(BaseEntitySchema):
    """Product schema extending base entity"""
    NAME = SchemaColumn("name", np.object_, nullable=False)
    PRICE = SchemaColumn("price", np.float64, nullable=False)
    CATEGORY_ID = SchemaColumn("category_id", np.int64, nullable=False)
    SKU = SchemaColumn("sku", np.object_, nullable=False)
```

### Pattern 2: Schema Composition

```python
class AddressSchema(BaseSchema):
    """Reusable address schema component"""
    STREET = SchemaColumn("street", np.object_, nullable=False)
    CITY = SchemaColumn("city", np.object_, nullable=False)
    STATE = SchemaColumn("state", np.object_, nullable=False)
    ZIP_CODE = SchemaColumn("zip_code", np.object_, nullable=False)
    COUNTRY = SchemaColumn("country", np.object_, nullable=False, default="US")

class CustomerWithAddressSchema(BaseSchema):
    """Customer schema with embedded address"""
    CUSTOMER_ID = SchemaColumn("customer_id", np.int64, nullable=False)
    NAME = SchemaColumn("name", np.object_, nullable=False)
    
    # Compose address fields with prefix
    BILLING_STREET = SchemaColumn("billing_street", np.object_, nullable=False)
    BILLING_CITY = SchemaColumn("billing_city", np.object_, nullable=False)
    BILLING_STATE = SchemaColumn("billing_state", np.object_, nullable=False)
    BILLING_ZIP = SchemaColumn("billing_zip_code", np.object_, nullable=False)
    
    SHIPPING_STREET = SchemaColumn("shipping_street", np.object_, nullable=True)
    SHIPPING_CITY = SchemaColumn("shipping_city", np.object_, nullable=True)
    SHIPPING_STATE = SchemaColumn("shipping_state", np.object_, nullable=True)
    SHIPPING_ZIP = SchemaColumn("shipping_zip_code", np.object_, nullable=True)
```

### Pattern 3: Dynamic Schema Validation

```python
def validate_with_business_rules(df: SchemaDataFrame, schema_class):
    """Enhanced validation with business rules"""
    
    # Standard schema validation
    errors = schema_class.validate_dataframe(df.df)
    
    # Custom business rule validations
    business_errors = []
    
    if hasattr(schema_class, 'PRICE'):
        # Price must be positive
        negative_prices = df[df[schema_class.PRICE] <= 0]
        if len(negative_prices) > 0:
            business_errors.append(f"Found {len(negative_prices)} records with negative prices")
    
    if hasattr(schema_class, 'EMAIL'):
        # Email format validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        invalid_emails = df[~df[schema_class.EMAIL].str.match(email_pattern, na=False)]
        if len(invalid_emails) > 0:
            business_errors.append(f"Found {len(invalid_emails)} records with invalid email format")
    
    if hasattr(schema_class, 'ORDER_DATE') and hasattr(schema_class, 'SHIP_DATE'):
        # Ship date must be after order date
        invalid_dates = df[
            (df[schema_class.SHIP_DATE].notna()) & 
            (df[schema_class.SHIP_DATE] < df[schema_class.ORDER_DATE])
        ]
        if len(invalid_dates) > 0:
            business_errors.append(f"Found {len(invalid_dates)} records with ship date before order date")
    
    return errors + business_errors
```

---

## 🔗 Integration Examples

### Integration 1: FastAPI with PandasSchemaster

```python
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import pandas as pd
from pandasschemaster import SchemaDataFrame, SchemaGenerator
import io

app = FastAPI()

class AnalysisRequest(BaseModel):
    file_type: str
    schema_name: str

@app.post("/analyze-data/")
async def analyze_data(file: UploadFile = File(...)):
    """API endpoint to analyze uploaded data with auto-generated schema"""
    
    try:
        # Read uploaded file
        contents = await file.read()
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file.filename.endswith('.json'):
            df = pd.read_json(io.StringIO(contents.decode('utf-8')))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Generate schema automatically
        generator = SchemaGenerator(sample_size=1000)
        schema_code = generator.generate_schema_from_dataframe(df, "APIGeneratedSchema")
        
        # Execute generated schema code
        exec(schema_code)
        schema_class = locals()['APIGeneratedSchema']
        
        # Create validated DataFrame
        validated_df = SchemaDataFrame(df, schema_class, validate=True)
        
        # Perform analysis
        analysis = {
            'rows': len(validated_df),
            'columns': len(validated_df.columns),
            'schema': schema_code,
            'summary': validated_df.describe().to_dict(),
            'data_types': validated_df.dtypes.astype(str).to_dict()
        }
        
        return analysis
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/validate-data/")
async def validate_data(file: UploadFile = File(...), schema_code: str = None):
    """Validate uploaded data against provided schema"""
    
    if not schema_code:
        raise HTTPException(status_code=400, detail="Schema code required")
    
    try:
        # Read data
        contents = await file.read()
        df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        
        # Execute provided schema
        exec(schema_code)
        # Assume schema class is the last defined class
        schema_class = None
        for name, obj in locals().items():
            if hasattr(obj, '__bases__') and 'BaseSchema' in str(obj.__bases__):
                schema_class = obj
        
        if not schema_class:
            raise HTTPException(status_code=400, detail="No valid schema found in provided code")
        
        # Validate
        errors = schema_class.validate_dataframe(df)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'rows_validated': len(df)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### Integration 2: Apache Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import pandas as pd
from pandasschemaster import SchemaDataFrame, SchemaGenerator

# Schema for daily sales data
class DailySalesSchema(BaseSchema):
    DATE = SchemaColumn("date", np.datetime64, nullable=False)
    STORE_ID = SchemaColumn("store_id", np.int64, nullable=False)
    PRODUCT_ID = SchemaColumn("product_id", np.object_, nullable=False)
    QUANTITY = SchemaColumn("quantity", np.int64, nullable=False)
    UNIT_PRICE = SchemaColumn("unit_price", np.float64, nullable=False)
    TOTAL_AMOUNT = SchemaColumn("total_amount", np.float64, nullable=False)

def extract_and_validate_data(**context):
    """Extract data and validate with schema"""
    
    # Extract data from source
    df = pd.read_csv('/data/daily_sales.csv')
    
    # Validate with schema
    validated_df = SchemaDataFrame(df, DailySalesSchema, validate=True)
    validation_errors = validated_df.validate_against_schema()
    
    if validation_errors:
        raise ValueError(f"Data validation failed: {validation_errors}")
    
    # Save validated data
    validated_df.to_csv('/data/validated_sales.csv', index=False)
    
    return len(validated_df)

def transform_sales_data(**context):
    """Transform validated data using schema columns"""
    
    # Load validated data
    df = pd.read_csv('/data/validated_sales.csv')
    validated_df = SchemaDataFrame(df, DailySalesSchema, validate=False)  # Already validated
    
    # Type-safe transformations
    validated_df['revenue_per_store'] = validated_df.groupby(
        DailySalesSchema.STORE_ID.name
    )[DailySalesSchema.TOTAL_AMOUNT.name].transform('sum')
    
    validated_df['avg_unit_price'] = validated_df.groupby(
        DailySalesSchema.PRODUCT_ID.name
    )[DailySalesSchema.UNIT_PRICE.name].transform('mean')
    
    # Save transformed data
    validated_df.to_csv('/data/transformed_sales.csv', index=False)

def generate_schema_for_new_data(**context):
    """Auto-generate schema for new data sources"""
    
    generator = SchemaGenerator()
    
    # Generate schemas for all new files
    import glob
    for file_path in glob.glob('/data/new/*.csv'):
        schema_code = generator.generate_schema_from_file(file_path)
        
        # Save schema to file
        schema_filename = file_path.replace('.csv', '_schema.py').replace('/data/new/', '/schemas/')
        with open(schema_filename, 'w') as f:
            f.write(schema_code)

# Define DAG
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'sales_data_pipeline',
    default_args=default_args,
    description='Daily sales data pipeline with PandasSchemaster',
    schedule_interval='@daily',
    catchup=False
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_and_validate',
    python_callable=extract_and_validate_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform_data',
    python_callable=transform_sales_data,
    dag=dag
)

schema_gen_task = PythonOperator(
    task_id='generate_schemas',
    python_callable=generate_schema_for_new_data,
    dag=dag
)

# Set task dependencies
extract_task >> transform_task
schema_gen_task  # Runs independently
```

### Integration 3: Jupyter Notebook Analysis

```python
# Cell 1: Setup and imports
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pandasschemaster import SchemaColumn, SchemaDataFrame, BaseSchema, SchemaGenerator

# Configure plotting
plt.style.use('default')
sns.set_palette("husl")

# Cell 2: Define schema for analysis
class WebAnalyticsSchema(BaseSchema):
    """Web analytics data schema"""
    SESSION_ID = SchemaColumn("session_id", np.object_, nullable=False)
    USER_ID = SchemaColumn("user_id", np.int64, nullable=True)
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    PAGE_URL = SchemaColumn("page_url", np.object_, nullable=False)
    REFERRER = SchemaColumn("referrer", np.object_, nullable=True)
    USER_AGENT = SchemaColumn("user_agent", np.object_, nullable=False)
    SESSION_DURATION = SchemaColumn("session_duration", np.int64, nullable=True)
    BOUNCE_RATE = SchemaColumn("bounce_rate", np.float64, nullable=True)
    CONVERSION = SchemaColumn("conversion", np.bool_, nullable=False, default=False)

# Cell 3: Load and validate data
def load_web_data(file_path):
    """Load and validate web analytics data"""
    
    print("🔄 Loading web analytics data...")
    df = pd.read_csv(file_path)
    
    print("✅ Validating data with schema...")
    validated_df = SchemaDataFrame(df, WebAnalyticsSchema, validate=True, auto_cast=True)
    
    errors = validated_df.validate_against_schema()
    if errors:
        print("❌ Validation errors found:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✅ Data validation successful!")
    
    print(f"📊 Loaded {len(validated_df)} records with {len(validated_df.columns)} columns")
    return validated_df

# Load data
web_df = load_web_data('web_analytics.csv')

# Cell 4: Exploratory analysis with type-safe operations
def explore_web_data(df: SchemaDataFrame):
    """Exploratory analysis using schema columns"""
    
    print("🔍 Web Analytics Exploration")
    print("=" * 40)
    
    # Basic stats using schema columns
    print(f"Total sessions: {df[WebAnalyticsSchema.SESSION_ID].nunique():,}")
    print(f"Unique users: {df[WebAnalyticsSchema.USER_ID].nunique():,}")
    print(f"Conversion rate: {df[WebAnalyticsSchema.CONVERSION].mean() * 100:.2f}%")
    print(f"Average session duration: {df[WebAnalyticsSchema.SESSION_DURATION].mean():.1f} seconds")
    
    # Time-based analysis
    df['hour'] = df[WebAnalyticsSchema.TIMESTAMP].dt.hour
    df['day_of_week'] = df[WebAnalyticsSchema.TIMESTAMP].dt.day_name()
    
    # Top pages
    top_pages = df[WebAnalyticsSchema.PAGE_URL].value_counts().head(10)
    print(f"\nTop 10 pages:\n{top_pages}")
    
    return df

# Run exploration
web_df = explore_web_data(web_df)

# Cell 5: Visualization using schema columns
def create_visualizations(df: SchemaDataFrame):
    """Create visualizations using type-safe column access"""
    
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Sessions by hour using schema column
    hourly_sessions = df.groupby('hour').size()
    axes[0, 0].plot(hourly_sessions.index, hourly_sessions.values, marker='o')
    axes[0, 0].set_title('Sessions by Hour of Day')
    axes[0, 0].set_xlabel('Hour')
    axes[0, 0].set_ylabel('Number of Sessions')
    
    # 2. Conversion rate by day using schema column
    daily_conversion = df.groupby('day_of_week')[WebAnalyticsSchema.CONVERSION.name].mean()
    axes[0, 1].bar(daily_conversion.index, daily_conversion.values)
    axes[0, 1].set_title('Conversion Rate by Day of Week')
    axes[0, 1].set_ylabel('Conversion Rate')
    axes[0, 1].tick_params(axis='x', rotation=45)
    
    # 3. Session duration distribution using schema column
    duration_data = df[WebAnalyticsSchema.SESSION_DURATION].dropna()
    axes[1, 0].hist(duration_data, bins=50, alpha=0.7, edgecolor='black')
    axes[1, 0].set_title('Session Duration Distribution')
    axes[1, 0].set_xlabel('Duration (seconds)')
    axes[1, 0].set_ylabel('Frequency')
    
    # 4. Bounce rate vs session duration using schema columns
    valid_data = df[
        df[WebAnalyticsSchema.BOUNCE_RATE].notna() & 
        df[WebAnalyticsSchema.SESSION_DURATION].notna()
    ]
    axes[1, 1].scatter(
        valid_data[WebAnalyticsSchema.SESSION_DURATION], 
        valid_data[WebAnalyticsSchema.BOUNCE_RATE],
        alpha=0.6
    )
    axes[1, 1].set_title('Bounce Rate vs Session Duration')
    axes[1, 1].set_xlabel('Session Duration (seconds)')
    axes[1, 1].set_ylabel('Bounce Rate')
    
    plt.tight_layout()
    plt.show()

# Create visualizations
create_visualizations(web_df)
```

---

## ⚡ Performance Examples

### Example 1: Large Dataset Processing

```python
import pandas as pd
from pandasschemaster import SchemaDataFrame, SchemaGenerator
import time
from memory_profiler import profile

class LargeDataSchema(BaseSchema):
    """Schema for large dataset processing"""
    ID = SchemaColumn("id", np.int64, nullable=False)
    CATEGORY = SchemaColumn("category", np.object_, nullable=False)
    VALUE = SchemaColumn("value", np.float64, nullable=False)
    TIMESTAMP = SchemaColumn("timestamp", np.datetime64, nullable=False)
    STATUS = SchemaColumn("status", np.bool_, nullable=False)

@profile
def process_large_dataset(file_path: str, chunk_size: int = 10000):
    """Memory-efficient processing of large datasets"""
    
    print(f"🚀 Processing large dataset with chunk size: {chunk_size:,}")
    
    results = []
    total_rows = 0
    
    # Process in chunks to manage memory
    for chunk_num, chunk in enumerate(pd.read_csv(file_path, chunksize=chunk_size)):
        start_time = time.time()
        
        # Validate chunk with schema (skip auto_cast for performance)
        chunk_df = SchemaDataFrame(chunk, LargeDataSchema, validate=True, auto_cast=False)
        
        # Type-safe operations on chunk
        chunk_summary = {
            'chunk_num': chunk_num,
            'rows': len(chunk_df),
            'avg_value': chunk_df[LargeDataSchema.VALUE].mean(),
            'category_counts': chunk_df[LargeDataSchema.CATEGORY].value_counts().to_dict(),
            'active_count': chunk_df[LargeDataSchema.STATUS].sum()
        }
        
        results.append(chunk_summary)
        total_rows += len(chunk_df)
        
        processing_time = time.time() - start_time
        print(f"Chunk {chunk_num}: {len(chunk_df):,} rows processed in {processing_time:.2f}s")
    
    print(f"✅ Total rows processed: {total_rows:,}")
    return results

def benchmark_schema_operations():
    """Benchmark schema operations vs regular pandas"""
    
    # Create test data
    n_rows = 100_000
    test_data = {
        'id': range(n_rows),
        'category': np.random.choice(['A', 'B', 'C', 'D'], n_rows),
        'value': np.random.randn(n_rows),
        'timestamp': pd.date_range('2024-01-01', periods=n_rows, freq='1min'),
        'status': np.random.choice([True, False], n_rows)
    }
    
    # Regular pandas DataFrame
    print("🐼 Regular pandas operations:")
    start_time = time.time()
    regular_df = pd.DataFrame(test_data)
    category_stats = regular_df.groupby('category')['value'].agg(['mean', 'sum', 'count'])
    pandas_time = time.time() - start_time
    print(f"Time: {pandas_time:.3f}s")
    
    # Schema DataFrame operations
    print("🛡️ Schema DataFrame operations:")
    start_time = time.time()
    schema_df = SchemaDataFrame(test_data, LargeDataSchema, validate=False)  # Skip validation for fair comparison
    schema_stats = schema_df.groupby(LargeDataSchema.CATEGORY.name)[LargeDataSchema.VALUE.name].agg(['mean', 'sum', 'count'])
    schema_time = time.time() - start_time
    print(f"Time: {schema_time:.3f}s")
    
    print(f"Overhead: {((schema_time - pandas_time) / pandas_time * 100):.1f}%")
    
    # Verify results are identical
    assert category_stats.equals(schema_stats), "Results should be identical"
    print("✅ Results verified identical")

# Run benchmarks
# benchmark_schema_operations()
```

### Example 2: Optimized Schema Generation

```python
def optimized_schema_generation():
    """Optimized schema generation for various scenarios"""
    
    generator = SchemaGenerator()
    
    # Test different sampling strategies
    test_files = [
        ('small_data.csv', None),           # Use all data
        ('medium_data.csv', 10_000),        # Sample 10K rows
        ('large_data.csv', 5_000),          # Sample 5K rows
        ('huge_data.csv', 1_000),           # Sample 1K rows
    ]
    
    results = {}
    
    for file_path, sample_size in test_files:
        print(f"📊 Processing {file_path} (sample: {sample_size or 'all'})")
        
        start_time = time.time()
        
        # Configure generator for this file size
        generator.sample_size = sample_size
        
        try:
            schema_code = generator.generate_schema_from_file(file_path)
            generation_time = time.time() - start_time
            
            results[file_path] = {
                'success': True,
                'time': generation_time,
                'sample_size': sample_size,
                'schema_length': len(schema_code)
            }
            
            print(f"✅ Generated in {generation_time:.2f}s")
            
        except Exception as e:
            results[file_path] = {
                'success': False,
                'error': str(e),
                'time': time.time() - start_time
            }
            print(f"❌ Failed: {e}")
    
    return results

def memory_efficient_validation():
    """Memory-efficient validation strategies"""
    
    class ValidationSchema(BaseSchema):
        ID = SchemaColumn("id", np.int64, nullable=False)
        NAME = SchemaColumn("name", np.object_, nullable=False)
        VALUE = SchemaColumn("value", np.float64, nullable=False)
    
    # Strategy 1: Chunk-based validation
    def validate_in_chunks(file_path: str, chunk_size: int = 10_000):
        all_errors = []
        chunk_count = 0
        
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            chunk_errors = ValidationSchema.validate_dataframe(chunk)
            if chunk_errors:
                all_errors.extend([f"Chunk {chunk_count}: {error}" for error in chunk_errors])
            chunk_count += 1
        
        return all_errors
    
    # Strategy 2: Sample-based validation
    def validate_sample(file_path: str, sample_size: int = 1_000):
        df = pd.read_csv(file_path, nrows=sample_size)
        return ValidationSchema.validate_dataframe(df)
    
    # Strategy 3: Column-by-column validation
    def validate_by_column(df: pd.DataFrame):
        errors = []
        
        for column_name, column_def in ValidationSchema.get_columns().items():
            if column_def.name in df.columns:
                series = df[column_def.name]
                if not column_def.validate(series):
                    errors.append(f"Column {column_def.name} validation failed")
            elif not column_def.nullable:
                errors.append(f"Required column {column_def.name} is missing")
        
        return errors
    
    return {
        'chunk_validation': validate_in_chunks,
        'sample_validation': validate_sample,
        'column_validation': validate_by_column
    }
```

---

These examples demonstrate the versatility and power of PandasSchemaster across different domains and use cases. The library provides type safety, validation, and clear code structure while maintaining full pandas compatibility and performance.
