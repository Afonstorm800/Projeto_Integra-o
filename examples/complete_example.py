"""
Complete Example: Data Integration Project
Demonstrates all features of the integration system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_processing import DataProcessor
from serialization import SerializationHandler
from jobs import Job, Pipeline, ProcessController
from api import APIClient, PublicAPIExamples
from database import DatabaseManager, DataOperations
from utils import setup_logging, LogContext, ValueOperations
from dashboard import DashboardGenerator
import logging


def example_data_processing():
    """Example: Data processing with Regular Expressions"""
    print("\n=== Data Processing Example ===")
    
    processor = DataProcessor()
    
    # Normalize text
    text = "  Hello   World!  @#$  "
    normalized = processor.normalize_text(text)
    print(f"Normalized text: '{normalized}'")
    
    # Validate patterns
    email = "user@example.com"
    is_valid = processor.validate_pattern(email, 'email')
    print(f"Email '{email}' is valid: {is_valid}")
    
    # Normalize phone
    phone = "11987654321"
    normalized_phone = processor.normalize_phone(phone)
    print(f"Normalized phone: {normalized_phone}")
    
    # Normalize CPF
    cpf = "12345678901"
    normalized_cpf = processor.normalize_cpf(cpf)
    print(f"Normalized CPF: {normalized_cpf}")
    
    # Mask sensitive data
    sensitive = "My email is john.doe@example.com"
    masked = processor.mask_sensitive_data(sensitive, 'email')
    print(f"Masked: {masked}")
    
    # Compose data
    template = "Hello {name}, your order #{order_id} is ready!"
    data = {"name": "John", "order_id": "12345"}
    composed = processor.compose_data(template, data)
    print(f"Composed: {composed}")


def example_serialization():
    """Example: Data serialization (JSON, XML, YAML)"""
    print("\n=== Serialization Example ===")
    
    handler = SerializationHandler()
    
    # Sample data
    data = {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ],
        "metadata": {
            "created": "2024-01-01",
            "version": "1.0"
        }
    }
    
    # Export to different formats
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    handler.export_json(data, os.path.join(data_dir, 'users.json'))
    print("Exported to JSON")
    
    handler.export_xml(data, os.path.join(data_dir, 'users.xml'))
    print("Exported to XML")
    
    handler.export_yaml(data, os.path.join(data_dir, 'users.yaml'))
    print("Exported to YAML")
    
    # Import and convert
    imported = handler.import_json(os.path.join(data_dir, 'users.json'))
    print(f"Imported {len(imported['users'])} users from JSON")
    
    # Convert between formats
    handler.convert(
        os.path.join(data_dir, 'users.json'),
        os.path.join(data_dir, 'users_converted.xml')
    )
    print("Converted JSON to XML")


def example_jobs():
    """Example: Job and Process Control"""
    print("\n=== Job Control Example ===")
    
    # Define job functions
    def load_data(context):
        print("Loading data...")
        return {"records": [1, 2, 3, 4, 5]}
    
    def process_data(context):
        print("Processing data...")
        records = context.get('job_load_result', {}).get('records', [])
        return {"processed": [x * 2 for x in records]}
    
    def save_data(context):
        print("Saving data...")
        processed = context.get('job_process_result', {}).get('processed', [])
        return {"saved_count": len(processed)}
    
    # Create pipeline
    pipeline = Pipeline("data_pipeline")
    
    # Add jobs with dependencies
    pipeline.add_job(Job("load", load_data))
    pipeline.add_job(Job("process", process_data, depends_on=["load"]))
    pipeline.add_job(Job("save", save_data, depends_on=["process"]))
    
    # Execute pipeline
    result = pipeline.run()
    
    # Get status
    status = pipeline.get_status_summary()
    print(f"Pipeline completed: {status['status_counts']}")
    print(f"Total duration: {status['total_duration']:.2f}s")


def example_api_access():
    """Example: Remote API access"""
    print("\n=== API Access Example ===")
    
    try:
        # Get GitHub user information
        user_data = PublicAPIExamples.get_github_user("torvalds")
        print(f"GitHub User: {user_data.get('name', 'N/A')}")
        print(f"Public Repos: {user_data.get('public_repos', 'N/A')}")
        
        # Get random user
        random_user = PublicAPIExamples.get_random_user()
        if 'results' in random_user and random_user['results']:
            user = random_user['results'][0]
            print(f"Random User: {user['name']['first']} {user['name']['last']}")
        
        # Get exchange rates
        rates = PublicAPIExamples.get_exchange_rates('USD')
        if 'rates' in rates:
            print(f"USD to EUR: {rates['rates'].get('EUR', 'N/A')}")
            print(f"USD to GBP: {rates['rates'].get('GBP', 'N/A')}")
    
    except Exception as e:
        print(f"API access error (expected in some environments): {e}")


def example_database():
    """Example: Database operations"""
    print("\n=== Database Example ===")
    
    # Create SQLite database
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'example.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    db = DatabaseManager(f'sqlite:///{db_path}')
    
    # Create table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        category TEXT,
        price REAL,
        stock INTEGER
    )
    """
    db.execute_query(create_table_query)
    print("Created products table")
    
    # Insert data
    products = [
        {"id": 1, "name": "Laptop", "category": "Electronics", "price": 999.99, "stock": 10},
        {"id": 2, "name": "Mouse", "category": "Electronics", "price": 29.99, "stock": 50},
        {"id": 3, "name": "Keyboard", "category": "Electronics", "price": 79.99, "stock": 30},
        {"id": 4, "name": "Monitor", "category": "Electronics", "price": 299.99, "stock": 15},
        {"id": 5, "name": "Chair", "category": "Furniture", "price": 199.99, "stock": 20}
    ]
    db.bulk_insert("products", products)
    print(f"Inserted {len(products)} products")
    
    # Select data
    electronics = db.select("products", conditions={"category": "Electronics"})
    print(f"Found {len(electronics)} electronics products")
    
    # Grouping
    group_result = db.group_by(
        "products",
        group_columns=["category"],
        agg_columns={"price": "AVG", "stock": "SUM"}
    )
    print("Grouped by category:")
    for row in group_result:
        print(f"  {row}")
    
    # Data operations
    ops = DataOperations(db)
    aggregates = ops.aggregate(
        "products",
        operations={"price": "AVG", "stock": "SUM"}
    )
    print(f"Aggregates: {aggregates}")


def example_value_operations():
    """Example: Value operations"""
    print("\n=== Value Operations Example ===")
    
    ops = ValueOperations()
    
    # Transform values
    value = 42.567
    rounded = ops.transform(value, "round", {"decimals": 2})
    print(f"Rounded: {rounded}")
    
    # Aggregate
    values = [10, 20, 30, 40, 50]
    avg = ops.aggregate(values, "avg")
    print(f"Average of {values}: {avg}")
    
    # Apply formula
    data = {"a": 10, "b": 20, "c": 5}
    result = ops.apply_formula(data, "(a + b) * c")
    print(f"Formula result: {result}")
    
    # Convert units
    meters = ops.convert_units(100, "cm", "m")
    print(f"100 cm = {meters} m")
    
    # Calculate percentage
    percentage = ops.calculate_percentage(25, 100)
    print(f"25 out of 100 is {percentage}%")
    
    # Growth rate
    growth = ops.calculate_growth_rate(100, 150)
    print(f"Growth from 100 to 150: {growth}%")


def example_dashboard():
    """Example: Dashboard visualization"""
    print("\n=== Dashboard Example ===")
    
    dashboard = DashboardGenerator()
    
    # Sample data
    sales_data = {
        'month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'sales': [1200, 1400, 1100, 1600, 1800, 2000],
        'expenses': [800, 900, 850, 950, 1000, 1100]
    }
    
    # Create line chart
    line_chart = dashboard.create_line_chart(
        sales_data,
        x='month',
        y=['sales', 'expenses'],
        title='Monthly Sales and Expenses'
    )
    dashboard.add_figure(line_chart)
    
    # Create bar chart
    bar_chart = dashboard.create_bar_chart(
        sales_data,
        x='month',
        y='sales',
        title='Monthly Sales'
    )
    dashboard.add_figure(bar_chart)
    
    # Category data
    category_data = {
        'category': ['Electronics', 'Furniture', 'Clothing', 'Food'],
        'revenue': [45000, 25000, 15000, 35000]
    }
    
    # Create pie chart
    pie_chart = dashboard.create_pie_chart(
        category_data,
        labels='category',
        values='revenue',
        title='Revenue by Category'
    )
    dashboard.add_figure(pie_chart)
    
    # Generate dashboard HTML
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'dashboard.html')
    
    dashboard.generate_dashboard_html(output_file)
    print(f"Dashboard generated: {output_file}")


def complete_integration_example():
    """Complete integration example combining all features"""
    print("\n=== Complete Integration Example ===")
    
    # Setup logging
    log_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'integration.log')
    setup_logging(log_file=log_file, level=logging.INFO)
    logger = logging.getLogger("Integration")
    
    with LogContext(logger, "Complete Integration Pipeline"):
        # 1. Fetch data from API
        def fetch_api_data(context):
            logger.info("Fetching data from API...")
            try:
                data = PublicAPIExamples.get_github_user("torvalds")
                return {"api_data": data}
            except:
                return {"api_data": {"name": "Sample User", "public_repos": 100}}
        
        # 2. Process and normalize data
        def process_api_data(context):
            logger.info("Processing API data...")
            api_data = context.get('job_fetch_result', {}).get('api_data', {})
            
            processor = DataProcessor()
            name = api_data.get('name', 'Unknown')
            normalized_name = processor.normalize_text(name)
            
            return {
                "processed_data": {
                    "name": normalized_name,
                    "repos": api_data.get('public_repos', 0)
                }
            }
        
        # 3. Store in database
        def store_in_db(context):
            logger.info("Storing data in database...")
            processed = context.get('job_process_api_result', {}).get('processed_data', {})
            
            db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'integration.db')
            db = DatabaseManager(f'sqlite:///{db_path}')
            
            # Create table
            db.execute_query("""
                CREATE TABLE IF NOT EXISTS github_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    repos INTEGER
                )
            """)
            
            # Insert data
            db.insert("github_users", processed)
            
            return {"stored": True}
        
        # 4. Export results
        def export_results(context):
            logger.info("Exporting results...")
            processed = context.get('job_process_api_result', {}).get('processed_data', {})
            
            handler = SerializationHandler()
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
            
            # Export to multiple formats
            handler.export_json(processed, os.path.join(output_dir, 'result.json'))
            handler.export_xml(processed, os.path.join(output_dir, 'result.xml'))
            handler.export_yaml(processed, os.path.join(output_dir, 'result.yaml'))
            
            return {"exported": True}
        
        # 5. Generate dashboard
        def generate_dashboard(context):
            logger.info("Generating dashboard...")
            processed = context.get('job_process_api_result', {}).get('processed_data', {})
            
            dashboard = DashboardGenerator()
            
            # Create simple metrics visualization
            metrics_data = {
                'metric': ['Repositories', 'Score'],
                'value': [processed.get('repos', 0), processed.get('repos', 0) * 10]
            }
            
            chart = dashboard.create_bar_chart(
                metrics_data,
                x='metric',
                y='value',
                title='GitHub Metrics'
            )
            dashboard.add_figure(chart)
            
            output_file = os.path.join(
                os.path.dirname(__file__), '..', 'data', 'integration_dashboard.html'
            )
            dashboard.generate_dashboard_html(output_file)
            
            return {"dashboard_created": True}
        
        # Create and execute pipeline
        pipeline = Pipeline("integration_pipeline")
        
        pipeline.add_job(Job("fetch", fetch_api_data))
        pipeline.add_job(Job("process_api", process_api_data, depends_on=["fetch"]))
        pipeline.add_job(Job("store", store_in_db, depends_on=["process_api"]))
        pipeline.add_job(Job("export", export_results, depends_on=["process_api"]))
        pipeline.add_job(Job("dashboard", generate_dashboard, depends_on=["process_api"]))
        
        # Run pipeline
        result = pipeline.run()
        
        # Display status
        status = pipeline.get_status_summary()
        logger.info(f"Pipeline completed with status: {status['status_counts']}")
        
        print("\nIntegration pipeline completed successfully!")
        print(f"Processed data: {result.get('job_process_api_result')}")
        print(f"Check the 'data' folder for outputs")


def main():
    """Run all examples"""
    print("=" * 60)
    print("Data Integration System - Complete Example")
    print("=" * 60)
    
    try:
        example_data_processing()
        example_serialization()
        example_jobs()
        example_api_access()
        example_database()
        example_value_operations()
        example_dashboard()
        complete_integration_example()
        
        print("\n" + "=" * 60)
        print("All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
